import sympy as sp
from pystencils import Assignment, Field
from lbmpy.boundaries.boundaryhandling import LbmWeightInfo
from pystencils.data_types import create_type
from pystencils.sympyextensions import get_symmetric_part
from lbmpy.simplificationfactory import create_simplification_strategy
from lbmpy.advanced_streaming.indexing import NeighbourOffsetArrays


class LbBoundary:
    """Base class that all boundaries should derive from"""

    inner_or_boundary = True
    single_link = False

    def __init__(self, name=None):
        self._name = name

    def __call__(self, f_out, f_in, dir_symbol, inv_dir, lb_method, index_field):
        """
        This function defines the boundary behavior and must therefore be implemented by all boundaries.
        The boundary is defined through a list of sympy equations from which a boundary kernel is generated.


        :param f_out: a pystencils field acting as a proxy to access the populations streaming out of the current
                cell, i.e. the post-collision PDFs of the previous LBM step
        :param f_in: a pystencils field acting as a proxy to access the populations streaming into the current
                cell, i.e. the pre-collision PDFs for the next LBM step
        :param dir_symbol: a sympy symbol that can be used as an index to f_out and f_in. It describes the direction
                    pointing from the fluid to the boundary cell.
        :param inv_dir: an indexed sympy symbol which describes the inversion of a direction index. It can be used in
                the indices of f_out and f_in for retrieving the PDF of the inverse direction.
        :param lb_method: an instance of the LB method used. Use this to adapt the boundary to the method
                    (e.g. compressibility)
        :param index_field: the boundary index field that can be used to retrieve and update boundary data

        :return: list of pystencils assignments, or pystencils.AssignmentCollection
        """
        raise NotImplementedError("Boundary class has to overwrite __call__")

    @property
    def additional_data(self):
        """Return a list of (name, type) tuples for additional data items required in this boundary
        These data items can either be initialized in separate kernel see additional_data_kernel_init or by
        Python callbacks - see additional_data_callback """
        return []

    @property
    def additional_data_init_callback(self):
        """Return a callback function called with a boundary data setter object and returning a dict of
        data-name to data for each element that should be initialized"""
        return None

    def get_additional_code_nodes(self, lb_method):
        """Return a list of code nodes that will be added in the generated code before the index field loop."""
        return []

    @property
    def name(self):
        if self._name:
            return self._name
        else:
            return type(self).__name__

    @name.setter
    def name(self, new_value):
        self._name = new_value

# end class Boundary


class NoSlip(LbBoundary):

    def __init__(self, name=None):
        """Set an optional name here, to mark boundaries, for example for force evaluations"""
        super(NoSlip, self).__init__(name)

    """
        No-Slip, (half-way) simple bounce back boundary condition, enforcing zero velocity at obstacle.
        Extended for use with any streaming pattern.
    """

    def __call__(self, f_out, f_in, dir_symbol, inv_dir, lb_method, index_field):
        return Assignment(f_in(inv_dir[dir_symbol]), f_out(dir_symbol))

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if not isinstance(other, NoSlip):
            return False
        return self.name == other.name

# end class NoSlip


class UBB(LbBoundary):
    """Velocity bounce back boundary condition, enforcing specified velocity at obstacle"""

    def __init__(self, velocity, adapt_velocity_to_force=False, dim=None, name=None):
        """
        Args:
            velocity: can either be a constant, an access into a field, or a callback function.
                      The callback functions gets a numpy record array with members, 'x','y','z', 'dir' (direction)
                      and 'velocity' which has to be set to the desired velocity of the corresponding link
            adapt_velocity_to_force:
        """
        super(UBB, self).__init__(name)
        self._velocity = velocity
        self._adaptVelocityToForce = adapt_velocity_to_force
        if callable(self._velocity) and not dim:
            raise ValueError("When using a velocity callback the dimension has to be specified with the dim parameter")
        elif not callable(self._velocity):
            dim = len(velocity)
        self.dim = dim

    @property
    def additional_data(self):
        if callable(self._velocity):
            return [('vel_%d' % (i,), create_type("double")) for i in range(self.dim)]
        else:
            return []

    @property
    def additional_data_init_callback(self):
        if callable(self._velocity):
            return self._velocity

    def get_additional_code_nodes(self, lb_method):
        return [LbmWeightInfo(lb_method), NeighbourOffsetArrays(lb_method.stencil)]

    def __call__(self, f_out, f_in, dir_symbol, inv_dir, lb_method, index_field):
        vel_from_idx_field = callable(self._velocity)
        vel = [index_field(f'vel_{i}') for i in range(self.dim)] if vel_from_idx_field else self._velocity
        direction = dir_symbol

        assert self.dim == lb_method.dim, \
            f"Dimension of UBB ({self.dim}) does not match dimension of method ({lb_method.dim})"

        neighbor_offset = NeighbourOffsetArrays.neighbour_offset(direction, lb_method.stencil)

        velocity = tuple(v_i.get_shifted(*neighbor_offset)
                         if isinstance(v_i, Field.Access) and not vel_from_idx_field
                         else v_i
                         for v_i in vel)

        if self._adaptVelocityToForce:
            cqc = lb_method.conserved_quantity_computation
            shifted_vel_eqs = cqc.equilibrium_input_equations_from_init_values(velocity=velocity)
            velocity = [eq.rhs for eq in shifted_vel_eqs.new_filtered(cqc.first_order_moment_symbols).main_assignments]

        c_s_sq = sp.Rational(1, 3)
        weight_of_direction = LbmWeightInfo.weight_of_direction
        vel_term = 2 / c_s_sq \
            * sum([d_i * v_i for d_i, v_i in zip(neighbor_offset, velocity)]) \
            * weight_of_direction(direction, lb_method)

        # Better alternative: in conserved value computation
        # rename what is currently called density to "virtual_density"
        # provide a new quantity density, which is constant in case of incompressible models
        if not lb_method.conserved_quantity_computation.zero_centered_pdfs:
            cqc = lb_method.conserved_quantity_computation
            density_symbol = sp.Symbol("rho")
            pdf_field_accesses = [f_out(i) for i in range(len(lb_method.stencil))]
            density_equations = cqc.output_equations_from_pdfs(pdf_field_accesses, {'density': density_symbol})
            density_symbol = lb_method.conserved_quantity_computation.defined_symbols()['density']
            result = density_equations.all_assignments
            result += [Assignment(f_in(inv_dir[direction]),
                                  f_out(direction) - vel_term * density_symbol)]
            return result
        else:
            return [Assignment(f_in(inv_dir[direction]),
                               f_out(direction) - vel_term)]
# end class UBB


class FixedDensity(LbBoundary):

    def __init__(self, density, name=None):
        if name is None:
            name = "Fixed Density " + str(density)
        super(FixedDensity, self).__init__(name)
        self._density = density

    def __call__(self, f_out, f_in, dir_symbol, inv_dir, lb_method, index_field):
        """Boundary condition that fixes the density/pressure at the obstacle"""

        def remove_asymmetric_part_of_main_assignments(assignment_collection, degrees_of_freedom):
            new_main_assignments = [Assignment(a.lhs, get_symmetric_part(a.rhs, degrees_of_freedom))
                                    for a in assignment_collection.main_assignments]
            return assignment_collection.copy(new_main_assignments)

        cqc = lb_method.conserved_quantity_computation
        velocity = cqc.defined_symbols()['velocity']
        symmetric_eq = remove_asymmetric_part_of_main_assignments(lb_method.get_equilibrium(),
                                                                  degrees_of_freedom=velocity)
        substitutions = {sym: f_out(i) for i, sym in enumerate(lb_method.pre_collision_pdf_symbols)}
        symmetric_eq = symmetric_eq.new_with_substitutions(substitutions)

        simplification = create_simplification_strategy(lb_method)
        symmetric_eq = simplification(symmetric_eq)

        density_symbol = cqc.defined_symbols()['density']

        density = self._density
        equilibrium_input = cqc.equilibrium_input_equations_from_init_values(density=density)
        equilibrium_input = equilibrium_input.new_without_subexpressions()
        density_eq = equilibrium_input.main_assignments[0]
        assert density_eq.lhs == density_symbol
        transformed_density = density_eq.rhs

        conditions = [(eq_i.rhs, sp.Equality(dir_symbol, i))
                      for i, eq_i in enumerate(symmetric_eq.main_assignments)] + [(0, True)]
        eq_component = sp.Piecewise(*conditions)

        subexpressions = [Assignment(eq.lhs, transformed_density if eq.lhs == density_symbol else eq.rhs)
                          for eq in symmetric_eq.subexpressions]

        return subexpressions + [Assignment(f_in(inv_dir[dir_symbol]),
                                            2 * eq_component - f_out(dir_symbol))]
# end class FixedDensity


class NeumannByCopy(LbBoundary):

    def get_additional_code_nodes(self, lb_method):
        return [NeighbourOffsetArrays(lb_method.stencil)]

    def __call__(self, f_out, f_in, dir_symbol, inv_dir, lb_method, index_field):
        neighbour_offset = NeighbourOffsetArrays.neighbour_offset(dir_symbol, lb_method.stencil)
        return [Assignment(f_in(inv_dir[dir_symbol]), f_out(inv_dir[dir_symbol])),
                Assignment(f_out[neighbour_offset](dir_symbol), f_out(dir_symbol))]

    def __hash__(self):
        # All boundaries of these class behave equal -> should also be equal
        return hash("NeumannByCopy")

    def __eq__(self, other):
        return type(other) == NeumannByCopy
# end class NeumannByCopy


class StreamInConstant(LbBoundary):
    def __init__(self, constant, name=None):
        super(StreamInConstant, self).__init__(name)
        self._constant = constant

    def get_additional_code_nodes(self, lb_method):
        return [NeighbourOffsetArrays(lb_method.stencil)]

    def __call__(self, f_out, f_in, dir_symbol, inv_dir, lb_method, index_field):
        neighbour_offset = NeighbourOffsetArrays.neighbour_offset(dir_symbol, lb_method.stencil)
        return [Assignment(f_in(inv_dir[dir_symbol]), self._constant),
                Assignment(f_out[neighbour_offset](dir_symbol), self._constant)]

    def __hash__(self):
        # All boundaries of these class behave equal -> should also be equal
        return hash("StreamInConstant")

    def __eq__(self, other):
        return type(other) == StreamInConstant
# end class StreamInConstant
