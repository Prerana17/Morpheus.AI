## Detailed Description

Inter-celltype contact energies per length unit as defined in
[CPM](#_group__ML__CPM) ShapeSurface. Contact energies can be constant
values or expressions of global symbols or symbols of the involved cell
types.

-   **type1:** name of one celltype involved in the interaction

-   **type2:** name of the other celltype involved in the interaction

-   **value:** Contact energy. Expression based on **global** symbols
    and symbols defined in cell type 1 -- prefixed by namespace
    **cell1** (e.g. cell1.adhesive) and symbols defined in cell type 2
    -- prefixed by namespace **cell2**.

# CPM {#_group__ML__CPM}

CPM

## Modules {.unnumbered}

-   [Interaction](#_group__ML__Interaction)

-   [MonteCarloSampler](#_group__ML__MonteCarloSampler)

-   [ShapeSurface](#_group__ML__ShapeSurface)

## Detailed Description

Specifies parameters for a cellular Potts model (CPM) representation of
cells. Temporal simulation is provided by a MonteCarlo sampler that
evolves the spatial cell configuration on the basis of statistical
sampling of the defined Hamiltonian landscape and Metropolis kinetics
acceptance rate.

Basic Hamiltonian using [Interaction](#_group__ML__Interaction) and
[VolumeConstraint](#_group__ML__VolumeConstraint) :

![](form_2.png)

Additional contributions can be defined under
[CellType](#_group__ML__CellType) .

[Interaction](#_group__ML__Interaction) specifies interaction energies
![](form_3.png) for different inter-cellular
[Contact](#_group__ML__Contact). The interaction energy is given per
length unit as defined in [ShapeSurface](#_group__ML__ShapeSurface).
[MonteCarloSampler](#_group__ML__MonteCarloSampler) specifies the
temporal simulation parameters.

### References {#_group__ConnectivityConstraint_1References}

1.  Graner and Glazier, Phys Rev Lett, 1992

2.  Käfer, Hogeweg and Marée, PLoS Comp Biol, 2006

3.  Magno, Grieneisen and Marée, BMC Biophysics, 2015

# DelayProperty {#_group__ML__DelayProperty}

DelayProperty

Symbol with a cell-bound scalar value and a **delay** time until values
become current. The **initial** value and **history** is given by the
**value** attribute as a time dependent
[MathExpressions](#_group__MathExpressions)

Symbol with a cell-bound scalar value and a **delay** time before
assigned values become current. The initial value and history is given
by a [MathExpressions](#_group__MathExpressions)

# DelayVariable {#_group__ML__DelayVariable}

DelayVariable

Symbol with a scalar value and a **delay** time until an assigned values
become current. The **initial** value and **history** is given by the
**value** attribute as a time dependent
[MathExpressions](#_group__MathExpressions).

Symbol with a scalar value and a **delay** time before assigned values
become current. The initial value and history is given by a
[MathExpressions](#_group__MathExpressions).

# DiffEqn {#_group__ML__DiffEqn}

DiffEqn

Assignment of a rate equation to a symbol.

Ordinary differential equation ![](form_94.png) if ![](form_95.png) is a
[Variable](#_group__ML__Variable) or a
[Property](#_group__ML__Property).

Partial differential equation ![](form_96.png) where ![](form_95.png) is
a [Field](#_group__ML__Field) and ![](form_97.png) is its diffusion
coefficient.

DiffEqn are only allowed within [System](#_group__ML__System).

# DisplacementTracker {#_group__ML__DisplacementTracker}

DisplacementTracker

Track the cell displacement of a population.

Track the cell displacement of a population.

## Description {#_group__LengthConstraint_1Description}

Displacement_Tracker extracts the cell displacements within one
cellpopulation (might be extended upon necessity). The data is stored in
a text file. In addition, the mean square displacement and the total
displacement of the population is calculated and stored in the first
columns of the text file.

## Example {#_group__ML__Function_1Example}

        <DisplacementTracker time-step="100" celltype="CellType1" cluster-id="cluster">

# Domain {#_group__ML__Domain}

Domain

A **Domain** specifies a non-regular geometry that restricts the
simulation to a domain within the lattice. Boundary conditions can be
chosen to be either constant or no-flux, but are required to be
homogeneous.

The **Image** tag allows to import a domain shape from an TIFF image or
image stack. By convention, non-zero pixels are foreground, zero pixels
are background. If a pixel dimension of the image file is smaller than
the manually defined lattice size (x,y,z) then the domain gets centered
on the lattice, otherwise the lattice size gets extended to the larger
dimension of the image file. Note that explicit position-dependencies in
terms or attributes (e.g. for initialization of **CellPopulations**) may
need to be rescaled manually if a domain image does not match the
manually defined lattice size.

The **Circle** tag allows to define circular domain shapes. Extends to a
cylinder in 3D.

The **Hexagon** tag allows to define hexagonal domain shapes. Extends to
a honeycomb in 3D.

The **Expression** tag allows to define a domain shape by a boolean
mathematical expression. All values larger than zero are considered to
be part of the domain.

# Equation {#_group__ML__Equation}

Equation

Assignment of mathematical expression to a symbol.

During simulation it is asserted that the provided relation always
holds. The assignment is executed whenever the input might have changed
and/or the result is needed elsewhere.

For vector data, use [VectorEquation](#_group__ML__VectorEquation).

For recurrence equations (in which the expression depends on the output
symbol), use a [Rule](#_group__ML__Rule) within a
[System](#_classSystem).

## Example {#_group__ML__Function_1Example}

Assume \'a\' is a variable or property.

    <Equation symbol-ref="a">
        (u*v)/(1+v)
    </Equation>  

# Event {#_group__ML__Event}

Event

## Modules {.unnumbered}

-   [Constant](#_group__ML__Constant)

-   [ConstantVector](#_group__ML__ConstantVector)

-   [Function](#_group__ML__Function)

    Parametric Function declaration.

-   [Intermediate](#_group__ML__Intermediate)

-   [IntermediateVector](#_group__ML__IntermediateVector)

-   [Rule](#_group__ML__Rule)

-   [VectorFunction](#_group__ML__VectorFunction)

-   [VectorRule](#_group__ML__VectorRule)

## Detailed Description

Environment for conditionally executed set of assignments.

-   **time-step**: if specified, Condition is evaluated in regular
    intervals (*time-step*). If not specified, the minimal time-step of
    the input symbols is used.

-   **Condition:** expression that must evaluate true to trigger
    assignments.

-   **Condition/history**: initial value of the condition. Used to
    determine whether an initially true condition may trigger if
    *trigger=\"on-change\"*.

-   **Logging** (optional): Log all triggered events to file, including
    all symbols defined under this tag.

-   **trigger:** the event is triggered whenever the condition turns
    true (**on-change**, as in SBML) or whenever the condition is found
    true (**when-true**, also see *time-step*).

-   **delay:** time by which the execution of the assignments of the
    event is delayed.

-   **persistent:** a delayed event who\'s condition *fell* false during
    a delay does only execute if *persistent=\"true\"*. (default *true*)

-   **compute-time**: time at which the values of the assignments are
    computed *on-trigger* / *on-execution*.

### Example {#_group__ML__Function_1Example}

Set symbol \"c\" (e.g. assume it\'s a CellProperty) to 1 after 1000
simulation time units

    <Event trigger="on change" time-step="1">
        <Condition> time > 1000 </Condition>
        <Rule symbol-ref="c">
            <Expression>1</Expression>
        </Rule>
    </Event>

# External {#_group__ML__External}

External

Execute external shell script.

Execute external shell script.

## Description {#_group__LengthConstraint_1Description}

Executes shell command periodically or at the end of simulation, e.g. to
perform analysis using external command line tools.

Commands are executed via shell, which means that .bashrc or .profile
are read.

To customize the environment, one can set (override) environmental
variables (e.g. \$PATH).

Use \"%\" (percentage) to provide global symbols as arguments in the
script. For instance the substring \"%time\" will be replaced with the
symbol \"time\", the current simulation time.

Stdout and stderr are written to the file \"external\_#n_output.txt\"
and \"external\_#n_error.txt\", with #n being the nth instance of
**External**.

-   **detach:** Run the process in the background while continuing
    simulation. Note that **timeout** is the maximum time the command
    may run after the simulation finished.

-   **timeout:** Timeout for running the external process. Defaults to
    30 seconds. (Only applicable with **detach** enabled)

-   **Command:** Executable shell command, e.g. \"tail -n 1 logger.txt\"
    or \"python analysis.py\"

-   **Environment:** variable/value, e.g. PATH=\'\\usr\\local\\bin\'

## Example {#_group__ML__Function_1Example}

Periodically execute python script using simulation output folder as cwd

    <External time-step="100">
        <Command> python /home/USER/scripts/analysis.py" </Command>
        <Environment variable="PYTHONPATH" value="/usr/lib/python2.7/">
    </External>

Provide the current time as argument to a python script

    <External time-step="100">
        <Command> python /home/USER/scripts/analysis.py --time=%time" </Command>
    </External>

Execute script along the simulation in a background process.

    <External time-step="100" separate-thread="true">
        <Command> python /home/USER/scripts/analysis.py </Command>
    </External>

# Field {#_group__ML__Field}

Field

## Modules {.unnumbered}

-   [TIFFReader](#_group__TIFFReader)

## Detailed Description

A **Field** defines a variable scalar field, associating a scalar value
to every lattice site, and defines a symbol with it. Spatio-temporal
dynamics can be implemented explicitly by using an
[Equation](#_group__ML__Equation), an [Event](#_group__ML__Event) or by
using [DiffEqn](#_group__ML__DiffEqn), which also allows to specify
Reaction-(Advection)-Diffusion systems.

-   **value:** **initial** condition for the scalar field. May be given
    as [MathExpressions](#_group__MathExpressions), also depending on
    the spatial position (see [Space](#_group__ML__Space))

Optionally, a **Diffusion** rate may be specified.

-   **rate:** diffusion coefficient \[(node length)² per (global time)\]

-   **well-mixed** (optional): if true, homogenizes scalar field. If
    enabled, diffusion **rate** is ignored.

**!NOTE** From Morpheus version 2.3 onwards, diffusion is also affected
by the time-scaling of the [System](#_group__ML__System) controlling the
[Field](#_group__ML__Field)\'s temporal evolution. This change from
earlier versions was introduced to allow convenient time scaling of
whole PDEs.

**BoundaryValue** defines the boundary conditions of the
[Field](#_group__ML__Field) at the respective boundary. By default, the
[Lattice](#_group__ML__Lattice) boundary type definitions are set and
the default value/flux tuple is {0,-} for `constant`, and {resp. value
within space,0} for `noflux` and `flux` boundaries.**Note!** Boundaries
predefined as periodic are immutable.

-   **boundary:** a boundary of the model space.
    ([Lattice](#_group__ML__Lattice))

-   **value:** mathematical expression providing the value or the flux
    for the respective boundary type that may vary in space and time.

-   **type** (optional): type of boundary value. If no **type** is
    specified, the [Lattice](#_group__ML__Lattice) defined type is
    preserved.

    -   `value` (default): **value** attribute specifies the value at
        the boundary, leaving the boundary type untouched.

    -   `constant` and `noflux:` **value** attribute specifies the value
        at the boundary and the respective boundary condition,
        potentially overriding the predefined type.

    -   `flux:` **value** attribute specifies the influx at the
        boundary, i.e. the first order derivative at the boundary,
        potentially overriding the predefined boundary type.

**TiffReader:** specify the initial condition of the field in terms of a
float tiff image.

# Function {#_group__ML__Function}

Function

Parametric Function declaration.

Parametric Function declaration.

Functions define an expression that relates Parameters,
[Symbols](#_group__Symbols) from the [Scope](#_group__Scope) of the
Function definition and other **Functions** to a scalar result. A
Function captures the scope of it\'s definition, thus applying a
Function in a sub-scope will not make the sub-scope\'s symbol
definitions available.

Function definitions are available within their local
[Scope](#_group__Scope) and all sub-scopes therein.

For convenience, a parameter-free Function definition is also available
as a plain Symbol, thus you may call it without parentheses.

Functions are not explicitly scheduled. Instead they are evaluated
\'on-the-fly\' whenever their output is requested. Recursive function
calls are prohibited.

For vector data, use [VectorFunction](#_group__ML__VectorFunction).

To assign to a variable or property, use
[Equation](#_group__ML__Equation).

## Example {#_group__ML__Function_1Example}

A non-parametric function available as **a** and **a()** in mathematical
expressions

    <Field symbol="u" />
    <Variable symbol="v" value="2.4" />
    <Function symbol="a">
        (u*v)/(1+v)
    </Function>  

A parametric function available as **a(k1,k2)** in mathematical
expressions

    <Function symbol="a">
        <Parameter "k1" />
        <Parameter "k2" />
        <Expression> 
            1/(1+k1)(1+k2^2)
        </Expression>
    </Function>  

# Global {#_group__ML__Global}

Global

## Modules {.unnumbered}

-   [Constant](#_group__ML__Constant)

-   [ConstantVector](#_group__ML__ConstantVector)

-   [DelayVariable](#_group__ML__DelayVariable)

-   [Equation](#_group__ML__Equation)

-   [Event](#_group__ML__Event)

-   [Field](#_group__ML__Field)

-   [Function](#_group__ML__Function)

    Parametric Function declaration.

-   [Mapper](#_group__ML__Mapper)

    Map data from a spatial context into another symbol, usually
    reducing spatial resolution by a mapping function.

-   [NeighborhoodReporter](#_group__NeighborhoodReporter)

    Reports data about a node\'s or a cell\'s neighborhood or
    \'microenvironment\'.

-   [NeighborhoodVectorReporter](#_group__NeighborhoodVectorReporter)

    Reports data about a node\'s or a cell\'s neighborhood or
    \'microenvironment\' using Vector input.

-   [System](#_group__ML__System)

-   [Variable](#_group__ML__Variable)

-   [VariableVector](#_group__ML__VariableVector)

-   [VectorEquation](#_group__ML__VectorEquation)

-   [VectorField](#_group__ML__VectorField)

-   [VectorFunction](#_group__ML__VectorFunction)

-   [VectorMapper](#_group__ML__VectorMapper)

    Map vector data from a spatial context into another symbol, usually
    reducing spatial resolution by a mapping function.

## Detailed Description

Section to include mathematical variabes and equations in the global
[Scope](#_group__Scope). If not yet part of a (new) model, a
double-click on this section in the model tree will add it.

**Global** provides subsections for:

-   Global [Constant](#_group__ML__Constant) and
    [Variable](#_group__ML__Variable) that can be overwritten in local
    scopes such as [CellType](#_group__ML__CellType) and
    [System](#_group__ML__System). In this case, **Global** serves as
    default value at spatial locations not occupied by local scopes
    (cells) which supports modular model development and allows to plot
    (cellular) variables for the whole spatial domain using
    [Gnuplotter](#_group__Gnuplotter).

-   **ODE** systems: [System](#_group__ML__System) of
    [DiffEqn](#_group__ML__DiffEqn) operating on
    [Variable](#_group__ML__Variable)

-   **Reaction-diffusion** PDE systems: [System](#_group__ML__System) of
    [DiffEqn](#_group__ML__DiffEqn) operating on diffusive
    [Field](#_group__ML__Field)

-   Global **Events:** [Event](#_group__ML__Event) changing global
    variables.

### Examples {#_group__ML__VectorRule_1Examples}

-   Globally defined constant \'e\' and a variable \'v\'. These symbols
    can be overwritten in subscopes, in which case the global values act
    as defaults.

        <Global>
            <Constant symbol="e" value="2.7182818284"/>
            <Variable symbol="v" value="0.0"/>
        </Global>

-   ODE [System](#_classSystem) without cellular context, see
    ODE/PredatorPrey example

        <Global>
            <Variable symbol="R" value="0.5"/>
            <Variable symbol="C" value="1.0"/>
            <System solver="Runge-Kutta [fixed, O(4)]" time-step="0.1">
                <Constant symbol="r" value="0.1"/>
                <Constant symbol="b" value="0.1"/>
                <Constant symbol="c" value="0.5"/>
                <Constant symbol="d" value="0.01"/>
                <Constant symbol="K" value="1"/>
                <DiffEqn symbol-ref="R">
                    <Expression>r*R - b*R*C</Expression>
                </DiffEqn>
                <DiffEqn symbol-ref="C">
                    <Expression>c*b*R*C - d*C</Expression>
                </DiffEqn>
            </System>
        </Global>

-   PDE reaction-diffusion [System](#_classSystem) with two diffusive
    scalar fields \'a\' and \'i\'. See PDE/ActivatorInhibitor_2D
    example.

        <Global>
            <Field symbol="a" value="rand_norm(0.5,0.1)" name="activator">
                <Diffusion rate="0.02" />
            </Field>
            <Field symbol="i" value="0.1" name="inhibitor">
                <Diffusion rate="1" />
            </Field>
            <System solver="Runge-Kutta [fixed, O(4)]" time-step="5" name="Meinhardt">
                <Constant symbol="rho" value="0.001"/>
                <Constant symbol="rho_a" value="0.001"/>
                <Constant symbol="mu_i" value="0.03"/>
                <Constant symbol="mu_a" value="0.02"/>
                <Constant symbol="kappa" value="0.10"/>
                <DiffEqn symbol-ref="a">
                    <Expression>(rho/i)*((a^2)/(1 + kappa*a^2)) - mu_a * a + rho_a</Expression>
                </DiffEqn>
                <DiffEqn symbol-ref="i">
                    <Expression>rho*((a^2)/(1+kappa*a^2)) - mu_i *i</Expression>
                </DiffEqn>
            </System>
        </Global>

# HeterophilicAdhesion {#_group__ML__HeterophilicAdhesion}

HeterophilicAdhesion

Heterophilic adhesive interaction between neighboring CPM cells.

Heterophilic adhesive interaction between neighboring CPM cells.

Increases adhesion (i.e. decreases cell-contact energy) between
neighboring CPM cells based on heterophilic binding, represented in cell
or membrane properties.

-   **adhesive1/2**: Expression describing the amount of both adhesive
    molecules.

-   **strength** (default=\"1\"): Expression describing strength of
    adhesive bonds.

-   **equilibriumConstant** (optional): Value describing ratio of
    binding/unbinding rates between adhesive molecules at cell
    membranes. If omitted, defaults to saturated binding.

If no *equilibriumConstant* is provided, saturated binding is assumed
usind equation: ![](form_18.png) , with units energy per node length.

If an *equilibriumConstant* is provided, the equilibrium concentration
of bonds is calculated on the basis of binding / unbinding rate ratio of
the following reaction in a symmetric fashion:

![](form_19.png)

![](form_20.png)

See HeterophilicAdhesion::interaction() for details.

# HistogramLogger {#_group__ML__HistogramLogger}

HistogramLogger

Computation of frequency distributions and visualisation of histograms.

Computation of frequency distributions and visualisation of histograms.

## Description {#_group__LengthConstraint_1Description}

[HistogramLogger](#_classHistogramLogger) computes a frequency
distribution from user-specified cell properties. Optionally, plots them
in a histogram.

## Input {#_group__LengthConstraint_1Input}

-   interval(default = 0.0)

-   number-of-bins (default = 20): Number of bins.

-   minimum (default = min value): Minimum value. Is used to calculate
    widths of bins. If not specified, taken from data.

-   maximum (default = max value): Maximum value. Is used to calculate
    widths of bins. If not specified, taken from data.

-   normalized (default = false): Calculate the absolute frequency
    distribution (false) or normalize by the number of data point
    (true).

-   logarithmic_bins (default = false): Use logarithmic bin sizes (base
    10)

-   logarithmic_freq (default = false): Use logarithm frequencies (base
    10).

### Input symbol(s) {#_group__ML__HistogramLogger_1autotoc_md0}

-   Column:

    -   symbol-ref (required): Symbol to compute frequency distriubution
        from, written as column in histogram file

    -   celltype (optional): To report symbol from single cell type (in
        case of symbol-ref revers to cell [Property](#_classProperty)).
        If not defined, all celltypes are assumed.

    -   label (optional): Custom label to add to plot. If not defined,
        symbol name is used.

### Visualization {#_group__ML__HistogramLogger_1autotoc_md1}

-   Plot:

    -   terminal (required): Gnuplot output terminal (e.g. x11, wxt,
        png, pdf).

    -   minimum (optional): Fixed minimum frequency (default: 0) used in
        the plot. If not specified, taken from distribution.

    -   maximum (optional): Fixed maximum frequency (default: 0) used in
        the plot. If not specified, taken from distribution.

    -   log-commands (optional): Write Gnuplot command to file.

## Examples {#_group__ML__VectorRule_1Examples}

     <HistogramLogger interval="1">
        <Binning minimum="-0.1" normalized="true" maximum="1.1" number_bins="20"/>
        <Column symbol-ref="X" celltype="cells"/>
        <Column symbol-ref="Y" celltype="cells"/>
        <Plot minimum="0" maximum="1.0" terminal="png" persist="true"/>
    </HistogramLogger>

# HomophilicAdhesion {#_group__ML__HomophilicAdhesion}

HomophilicAdhesion

Homophilic adhesive interaction between neighboring CPM cells.

Homophilic adhesive interaction between neighboring CPM cells.

Change cell-contact energy by factor based on binding between two
identical adhesives ![](form_13.png) on adjacent cells (i.e. cadherins).

-   **adhesive:** Expression describing amount of adhesive molecules.
    This may be a symbol representing a cell or membrane property (e.g.
    \"c\") or an expression (e.g. \"10 \* c\").

-   **strength** (default=\"1\"): Expression describing strength of
    adhesion. This may be a symbol representing a cell or membrane
    property (e.g. \"s\") or an expression (e.g. \"10 \* s\").

-   **equilibriumConstant** (optional): Value describing ratio of
    binding/unbinding between adhesive molecules at cell membranes.

If no *equilibriumConstant* is given (default), the full bond saturation
is assumed by taking the minimum of adhesive in both cells:

![](form_15.png) , with units energy per node length.

If an *equilibriumConstant* is given, the equilibrium concentration of
bonds is calculated on the basis of binding / unbinding rate ratio of
reaction

![](form_16.png)

![](form_17.png) , with units energy per node length.

## Examples {#_group__ML__VectorRule_1Examples}

    <HomophilicAdhesion adhesive="c" strength="1" />

    <HomophilicAdhesion adhesive="10*c" />

# InitProperty {#_group__ML__InitProperty}

InitProperty

InitProperty sets the value of a cell-bound
[Property](#_group__ML__Property) or
[MembraneProperty](#_group__ML__MembraneProperty) during the
initialization of a cell.

Expressions are evaluated separately for each cell, such that properties
can become stochastic or dependent on cell-position.

Note the difference to initialization with CellType/Property:
InitProperty is called ONLY during initialization (at StartTime, see
[Time](#_group__ML__Time)). Therefore, InitProperty is NOT called for
cells created during simulation, e.g. using the
[AddCell](#_group__ML__AddCell) plugin.

# InitVectorProperty {#_group__ML__InitVectorProperty}

InitVectorProperty

InitVectorProperty sets the value of a cell-bound
[PropertyVector](#_group__ML__PropertyVector) during the initialization
of a cell of a specific population.

Expressions are evaluated separately for each cell, such that properties
can become stochastic or dependent on cell-position.

Note the difference to initialization with CellType/Property:
InitProperty is called ONLY during initialization (at StartTime, see
[Time](#_group__ML__Time)). Therefore, InitProperty is NOT called for
cells created during simulation, e.g. using the
[AddCell](#_group__ML__AddCell) plugin.

Syntax is comma-separated as given by **notation** : orthogonal - x,y,z
radial - r,φ,θ or radial - φ,θ,r

# Interaction {#_group__ML__Interaction}

Interaction

## Modules {.unnumbered}

-   [Contact](#_group__ML__Contact)

    Inter-celltype contact energies per length unit as defined in
    [CPM](#_group__ML__CPM) ShapeSurface. Contact energies can be
    constant values or expressions of global symbols or symbols of the
    involved cell types.

## Detailed Description

specifies interaction energies ![](form_9.png) for different
inter-cellular [Contact](#_group__ML__Contact). The interaction energy
is given per length unit as defined in [CPM](#_group__ML__CPM)
ShapeSurface.

-   **default:** default value for unspecified interactions

-   **negate:** negate all defined interaction values

# IntermediateVector {#_group__ML__IntermediateVector}

IntermediateVector

An IntermediateVector Symbol is available to all expressions within a
[System](#_classSystem). Intermediates are evaluated prior to any other
construct and may even depend on each other. Defining circular
dependencies is discouraged, though.

# Intermediate {#_group__ML__Intermediate}

Intermediate

An Intermediate Symbol is available to all expressions within a
[System](#_classSystem). Intermediates are evaluated prior to any other
construct and may even depend on each other. Defining circular
dependencies is discouraged, though.

# Lattice {#_group__ML__Lattice}

Lattice

## Modules {.unnumbered}

-   [Domain](#_group__ML__Domain)

## Detailed Description

Specifies the size and structure of the lattice.

The **class** attribute determines the structure of the regular lattice:

-   linear: 1D

-   square: 2D

-   hexagonal: 2D

-   cubic: 3D

**Size** determines the size of the lattice in (x,y,z). A symbol can be
specified to refer to the lattice size. **!NOTE**: Contrary to other
places, size is given in nodes. Thus for **hexagonal** lattices the
actual (othogonal) height is 0.866\*size.y .

**NodeLength** specifies the physical length of a lattice node.

**BoundaryConditions** specify the type of boundary condition for each
boundary:

-   periodic (a.k.a. wrapped)

-   noflux (a.k.a. zero Neumann), Default

-   flux (a.k.a. Neumann)

-   constant (a.k.a. Dirichlet) Left and right boundaries are denoted as
    -x and x, respectively, and for y and z alike. The actual values
    have to be specified as **BoundaryValue** in the respective
    [Field](#_group__ML__Field) or under
    [CellPopulations](#_group__ML__CellPopulations).

**Neighborhood** determines the default size of the neighborhood to be
used in calculations. Currently this is exclusively used for
ML_NeighborhoodReporter und the
[Global](#_group__NeighborhoodVectorReporter_1Global) tag. This can be
provided in terms of:

-   Distance: Maximal distance to take into account, in units of lattice
    nodes.

-   Order: Order of the neighborhood. E.g. in a 2D square lattice, 1^st^
    order = 4 direct neighbors (von Neumann), 2^nd^ order = 8 nearest
    neighbors (Moore), etc.

[Domain](#_group__ML__Domain) specifies a non-regular geometry to
restrict the simulation to a domain within the lattice.

# Mapper {#_group__ML__Mapper}

Mapper

Map data from a spatial context into another symbol, usually reducing
spatial resolution by a mapping function.

Map data from a spatial context into another symbol, usually reducing
spatial resolution by a mapping function.

(formerly known as CellReporter)

## Description {#_group__LengthConstraint_1Description}

A **Mapper** defines how data within a spatial context, e.g. a cell, a
cell population or at global scope, can be mapped to a symbol with a
different spatial granularity (i.e. resolution). Note that defining a
Mapper within a [CellType](#_group__ML__CellType) also restricts the
mapping to the spatial range occupied by the respective cell population.

A single **Input** element must be specified:

-   **value:** input variable (e.g. [Property](#_group__ML__Property),
    [MembraneProperty](#_group__ML__MembraneProperty) or
    [Field](#_group__ML__Field)) or a respective expression.

That information can be written to an output symbol, if necessary,
reduced in spatial granularity by means of the **mapping** statistics.
If the output granularity is sufficient, i.e. when writing to a
[Field](#_group__ML__Field) or
[MembraneProperty](#_group__ML__MembraneProperty), no **mapping**
function needs to be specified.

Multiple **Output** elements can be specified:

-   **mapping:** statistic used for data mapping (if needed)

-   **symbol-ref**: ouput symbol (referencing e.g. a
    [Variable](#_group__ML__Variable), a
    [Property](#_group__ML__Property) or a
    [MembraneProperty](#_group__ML__MembraneProperty))

Via the **Polarisation** tag, the degree of polarization in a spatial
distribution of a quantity wrt. the center of the spatial range can be
mapped into a vector, heading into the direction of the maximum
quantity.

## Example {#_group__ML__Function_1Example}

Count number of cells within a celltype or globally. (Assume \'A\'
refers to Variable)

    <Mapper>
        <Input value="cell.id>0" />
        <Output symbol-ref="A" mapping="sum" />
    </Mapper>

Compute the sum and the variance of concentrations in a Field. (Assume
\'A\' refers to a Field and \'B1\' and \'B2\' to global Variables)

    <Mapper>
        <Input value="A" />
        <Output symbol-ref="B1" mapping="sum" />
        <Output symbol-ref="B2" mapping="variance" />
    </Mapper>

Average concentration of an agent in a Field in the range of a cell.
(Assume \'A\' to refer to a Field and \'B\' refer to a CellProperty)

    <Mapper>
        <Input value="A" />
        <Output symbol-ref="B" mapping="avg" />
    </Mapper>

Polarisation and variance of a membrane property (Assume B to refer to a
CellProperty, C to refer to a
[MembraneProperty](#_classMembraneProperty) and D to refer to a
VectorProperty)

    <Mapper>
        <Input value="C" />
        <Output symbol-ref="B" mapping="variance" />
        <Polarisation symbol-ref="D" />
    </Mapper>

Compute the binding rate of a soluble substance (A) to a membrane bound
molecule (C). (Assume \'A\' to refer to a Field and \'C\' and \'C_r\' to
refer to MembraneProperties)

    <Mapper>
        <Input value="C*A"/>
        <Output symbol-ref="C_r" />
    </Mapper>

# MechanicalLink {#_group__ML__MechanicalLink}

MechanicalLink

Spring-like mechanics excerted by links between cells. Equilibrium link
distance is reached when the distance of their centers equals the sum of
their radii assuming circular / spherical cell shape. Links always
detach with a certain probability given by an expression, but may form
only when cells are in touch. All expressions provide the scopes of the
involved cells via the named scopes **cell1** and **cell2** ( property
\'k1\' from the first cell is thus **cell1.k1** ).

-   **strength:** Spring constant of a link that determines the springs
    energy when multiplied with the relative stretch of the spring link.

-   **link-scaling**: Link strength is either independend of the
    interface length (cell) or proportional to the interface length of
    the cell (length), i.e. the strength represents actually a force
    density.

-   **link-probability**: Probability to establish a link with a
    touching cell.

-   **unlink-probability**: Probability to release an established link.
    Local variables **stretch.abs** and **stretch.rel** provide the
    absolute and relative stretch of the respective bond.

The implementation is inspired by the paper below, but allows for much
broader parameterisations. Use the **CellLinks** plot option of the
[Gnuplotter](#_group__Gnuplotter) to vizualize the link data. Currently,
only links amoung cells of the same cell type may be created. Future
versions will drop this limitation.

András Szabó, Manuela Melchionda, Giancarlo Nastasi, Mae L. Woods,
Salvatore Campo, Roberto Perris, Roberto Mayor; *In vivo confinement
promotes collective migration of neural crest cells.* J Cell Biol 6 June
2016; 213 (5): 543--555. doi: <https://doi.org/10.1083/jcb.201602083>.

# MembraneLattice {#_group__ML__MembraneLattice}

MembraneLattice

Defines the discretization of the membrane property system
([MembraneProperty](#_group__ML__MembraneProperty)), which is
represented by a field on a unit sphere / circle, that is mapped to the
actual cell boundary.

**Resolution** specifies the lattice discretization of the
membrane-bound fields. This resolution is equal for all
MembraneProperties and for all cells. By convention, the x and
y-resolution in 2D MembraneProperties are identical.

Optionally, a **Symbol** can be specified to refer to the lattice
discretization.

**SpaceSymbol** can be specified to refer to the current location with
respect to a membrane property. Positions are given as a vector (x,y,z)
or radial coords (r,φ,θ) on the unit sphere / circle representing the
membrane field. This can be used to initialize membrane properties (see
example below).

## Note {#_group__ConnectivityConstraint_1Note}

The resolution can have serious impact on computational performance, in
particular for reaction-diffusion systems on membranes of large cell
populations.

## Example {#_group__ML__Function_1Example}

To specify a membrane property with a lattice discretization of 100 and
definition of symbols for the membrane size and location (from PCP
example):

    <MembraneLattice>
        <Resolution symbol="memsize" value="100"/>
        <SpaceSymbol symbol="m"/>
    </MembraneLattice>

Note that the symbols defined above can be used to initialize the
membrane property, independent of the lattice discretization. Here,
using a sine wave, scaled between 0 and 1 by just referring to the angle
**φ** of the membrane position relative to the cell center.

    <MembraneProperty symbol-ref="membrane" value="0.5*sin(m.phi) + 0.5)" />

# MembraneProperty {#_group__ML__MembraneProperty}

MembraneProperty

Symbol represented by a variable scalar field that is mapped to the cell
membrane. Each boundary lattice site of the cell domain is thus
associated with a scalar value.

A [MembraneProperty](#_classMembraneProperty) is a circular (2D) or
spherical (3D) lattice mapped to the surface nodes of a cell using polar
coordinates. The underlying coordinate system, centered on each cell,
and its discretisation are defined in the
[MembraneLattice](#_group__ML__MembraneLattice).

**Diffusion** describes the diffusion within the underlying field, while
lengths are scaled to fit the cell perimeter / surface. That means
diffusion rates must be specified for the actual cell surface extends.
Diffusion computation is then performed on a circle / sphere taking the
cell\'s area / volume. **!NOTE** From Morpheus version 2.3 onwards,
diffusion is also affected by the time-scaling of the
[System](#_group__ML__System) controlling the Fields temporal evolution.
This change from earlier versions was introduced to allow convenient
time scaling of whole PDEs.

-   **value:** **initial** condition for the scalar field. May be given
    as a [MathExpressions](#_group__MathExpressions). Use the
    **SpaceSymbol** of the
    [MembraneLattice](#_group__ML__MembraneLattice) to define spatial
    heterogeneity.

Assuming *m* to be membrane space symbol we can initialize two
horizontal peaks:

    <MembraneProperty symbol-ref="membrane" value="1 + sin(2*m.phi)" />

Spatio-temporal **dynamics** can optionally be defined using a
[DiffEqn](#_group__ML__DiffEqn) or an [Event](#_group__ML__Event).

# MonteCarloSampler {#_group__ML__MonteCarloSampler}

MonteCarloSampler

**MonteCarloSampler** specifies all parameters for the the temporal
simulation of the CPM.

The Metropolis kinetics acceptance probability is defined as

![](form_7.png)

![](form_8.png)

-   **stepper:**

    -   **edgelist** chooses updates from a tracked list of lattice
        sites that can potentially change configuration

    -   **random** sampling chooses a lattice site with uniform random
        distribution over all lattice sites.

-   **MetropolisKinetics:**

    -   **temperature:** specifies Boltzmann probability used to accept
        updates that increase energy. Required to be homogeneous in
        space.

    -   **yield:** offset for Boltzmann probability distribution
        representing resistance to membrane deformations (see Kafer,
        Hogeweg and Maree, PLoS Comp Biol, 2006).

-   **Neighborhood** specifies the neighborhood size used for choosing
    updates in the modified Metropolis algorithm. The named neighborhood
    **optimal** represents 1st order for linear and hexagonal lattices,
    and 2nd order for square and cubic lattice.

-   **MCSDuration** scales the Monte Carlo Step (MCS) to global model
    time (a value of 10 will distribute one MCS over 10 model time
    units). One MCS is defined as a number of update attempts equal to
    the number of lattice sites.

# Population {#_group__ML__Population}

Population

## Modules {.unnumbered}

-   [CSVReader](#_group__CSVReader)

    Initializes cell population from CSV file.

-   [Cell](#_group__ML__Cell)

    Stores cell state.

-   [InitCellObjects](#_group__InitCellObjects)

    Initialize a population of cells with predefined geometrical objects
    in a regular lattice.

-   [InitCircle](#_group__InitCircle)

    Initializes cells as single nodes arranged in a circle.

-   [InitDistribute](#_group__InitDistribute)

    Places and initializes cells randomly in space the lattice with
    certain probability.

-   [InitHexLattice](#_group__InitHexLattice)

    Initializes lattice of cell for CA-like models.

-   [InitPoissonDisc](#_group__InitPoissonDisc)

    Arranges cells approximately equidistantly according to Poisson Disk
    Sampling.

-   [InitProperty](#_group__ML__InitProperty)

-   [InitRectangle](#_group__InitRectangle)

    Initializes cells as single nodes arranged in a rectangle.

-   [InitVectorProperty](#_group__ML__InitVectorProperty)

-   [InitVoronoi](#_group__InitVoronoi)

    Compute cell areas according to the Voronoi tesselation.

-   [TIFFReader](#_group__TIFFReader)

## Detailed Description

Specify the spatial configuration and cell states of a cell population.
Multiple populations are allowed for the same
[CellType](#_group__ML__CellType).

Spatial configuration can be seeded by [Population Initializer
Plugins](#_group__InitializerPlugins), directly generated by
InitCellObjects, or loaded cell by cell from **Cell** definitions. These
options may also be intermixed (Sequence matters here!).

Cell property initialisation can be overridden for the specific
[Population](#_group__ML__Population) using
[InitProperty](#_group__ML__InitProperty) and
[InitVectorProperty](#_group__ML__InitVectorProperty).

If SaveInterval is specified (see [Time](#_group__ML__Time)), the
simulation state for each cell in a population is written to
Population/Cell elements in the xml.gz file.

# PropertyVector {#_group__ML__PropertyVector}

PropertyVector

Symbol with cell-bound, variable 3D vector value. The **initial** value
is given by the **value** attribute as a
[MathExpressions](#_group__MathExpressions) and may depend on the
**cell.center** and contain stochasticity to create population
diversity.

Syntax is comma-separated as given by **notation** :

-   orthogonal - x,y,z

-   radial - r,φ,θ

-   or radial - φ,θ,r

# Property {#_group__ML__Property}

Property

Symbol with a cell-bound, variable scalar value. The **initial** value
is given by the **value** attribute as a
[MathExpressions](#_group__MathExpressions) and may depend on the
**cell.center** and contain stochasticity to create population
diversity.

# Rule {#_group__ML__Rule}

Rule

Assignment of mathematical expression to a symbol.

Differs from [Equation](#_group__ML__Equation) in that a Rule:

-   may contain recurrence relations e.g. ![](form_98.png)

-   can only appear in [System](#_group__ML__System)

-   explicitly scheduled based on user-specified [System](#_classSystem)
    time-step

## Examples {#_group__ML__VectorRule_1Examples}

Assign a new value to \'a\' based on values of \'a\' in previous
time-step.

    <System solver="euler" time-step="1">
        <Constant symbol="n" value="2">
        <Rule symbol-ref="a">
            <Expression> a^n / (a^n+1) </Expression>
        </Rule>  
    </System>

# ShapeSurface {#_group__ML__ShapeSurface}

ShapeSurface

**ShapeSurface** specifies the Neighborhood used to estimate the
boundary length of CPM Shapes, in particular cells. This estimate is
used for computing interaction energies, cell perimeters and interface
lengths.

-   **scaling** scaling of number of neighbors to length :

    -   **norm** estimate the length in unit of node length (see Magno,
        Grieneisen and Marée, BMC Biophysics, 2015),

    -   **none** estimate the length as the number of neighbor nodes
        occupied by other entities,

    -   **size** estimate the length as the neigborhood fraction
        occupied by other entities,

    -   **classic** estimate surface length by unscaled 1st order
        neighborhood - as used by CompuCell3D - and contact energies
        unscaled by the given neighborhood.

-   **Neigborhood** defines the stencil size to approximate the surface
    length. Wrt. shape isotropy some neighborhoods are favourable on a
    given lattice and are represented by the neighborhood named
    **optimal** :

    -   square -- 4th order corresponding to a distance of
        ![](form_4.png)

    -   hexagonal -- 4rd order, corresponding to a distance of
        ![](form_5.png)

    -   cubic -- 6th order corresponding to a distance of
        ![](form_6.png)

[Interaction](#_group__ML__Interaction) specifies interaction energies
![](form_3.png) for different inter-cellular
[Contact](#_group__ML__Contact). The interaction energy is given per
length unit as defined in ShapeSurface.

# SpaceSymbol {#_group__ML__SpaceSymbol}

SpaceSymbol

Specifies a symbol referring to the current location as a 3D vector
(x,y,z).

This symbol can then be used to make aspects dependent on space, such as
a gradient field.

## Example {#_group__ML__Function_1Example}

To create a gradient along the x direction from 0 to 1, first specify a
SpaceSymbol:

    <Space>
        <Lattice class="square">
            <Size symbol="size" value="20 20 0"/>
        </Lattice>
        <SpaceSymbol symbol="l" name="location"/>
    </Space>

And then create a [Field](#_group__ML__Field) ![](form_1.png) with
location-dependent initial condition, using this symbol (see Example
Miscellaneous/FrenchFlag):

    <Global>
        <Field value="l.x / size.x" symbol="f" >
        </Field>
    <Global>

Or to render a parameter (mathematical term) spatially heterogeneous
(see Example PDE/TuringPatterns):

    <Function symbol="A">
        <Expression>0.07 + ((0.07 * l.y)/ size.y)</Expression>
    </Function>

# Space {#_group__ML__Space}

Space

## Modules {.unnumbered}

-   [Lattice](#_group__ML__Lattice)

-   [MembraneLattice](#_group__ML__MembraneLattice)

-   [SpaceSymbol](#_group__ML__SpaceSymbol)

## Detailed Description

The [Space](#_group__ML__Space) element specifies the size, structure
and boundary conditions of the spatial lattice.

The selected types of boundary conditions are identically valid for all
model components, while the exact values (for Dirichlet boundary
conditions, denoted **constant**) can be specified through
**BoundaryValue** in a [Field](#_group__ML__Field) or in
[CellPopulations](#_group__ML__CellPopulations) for the cell layer.

A [SpaceSymbol](#_group__ML__SpaceSymbol) can be used to create a symbol
representing the current (x,y,z) location. The symbol always provides
the location in orthogonal coordinates. It is not (yet) scaled by the
defined node length.

[MembraneLattice](#_group__ML__MembraneLattice) specifies the resolution
of membrane-bound **Fields**. These fields are represented in 2D by a
circle-wrapped periodic lattice (0..resolution-1, 0, 0) and in 3D by a
sphere-wrapped periodic lattice (0..resolution-1, 0..resolution/2-1, 0),
respectively. The **SpaceSymbol** refers to the index position within
the lattice.

### Examples {#_group__ML__VectorRule_1Examples}

Linear lattice with periodic boundary conditions. See example
Miscellaneous/ShellCA.

    <Space>
        <Lattice class="linear">
            <Size value="100, 0, 0"/>
            <BoundaryConditions>
                <Condition boundary="x" type="periodic"/>
            </BoundaryConditions>
        </Lattice>
    </Space>

Hexagonal lattice. See example ODE/LateralSignalling.

    <Space>
        <Lattice class="hexagonal">
            <Size value="20 20 0"/>
            <BoundaryConditions>
                <Condition boundary="x" type="periodic"/>
                <Condition boundary="y" type="periodic"/>
            </BoundaryConditions>
        </Lattice>
    </Space>

Space specification with image-based domain. See example CPM/Crypt and
note that mismatches of image size versus lattice size are partially
resolved automatically, see [Domain](#_group__ML__Domain).

    <Space>
        <Lattice class="square">
            <Size symbol="size" value="600 600 0"/>
            <Neighborhood>
                <Order>3</Order>
            </Neighborhood>
            <Domain boundary-type="noflux">
                <Image path="crypt.tif"/>
            </Domain>
        </Lattice>
        <SpaceSymbol symbol="l"/>
    </Space>

# System {#_group__ML__System}

System

## Modules {.unnumbered}

-   [Constant](#_group__ML__Constant)

-   [ConstantVector](#_group__ML__ConstantVector)

-   [DiffEqn](#_group__ML__DiffEqn)

-   [Function](#_group__ML__Function)

    Parametric Function declaration.

-   [Intermediate](#_group__ML__Intermediate)

-   [IntermediateVector](#_group__ML__IntermediateVector)

-   [Rule](#_group__ML__Rule)

-   [VectorFunction](#_group__ML__VectorFunction)

-   [VectorRule](#_group__ML__VectorRule)

## Detailed Description

Environment for tightly coupled [Rule](#_group__ML__Rule) and
[DiffEqn](#_group__ML__DiffEqn). Expressions within a
**[System](#_classSystem)** are synchronously updated and may contain
recurrence relations.

-   **solver:** numerical solver for DiffEqn:

    -   Adaptive time step solvers:

        -   **Dormand-Prince** - adaptive, uses 4/5th order **default**

        -   **Cash-Karp** - adaptive, uses 4/5th order

        -   **Bogacki-Shampine** - adaptive, uses 2/3rd order

    -   Fixed time step solvers

        -   **Euler** - 1st order

        -   **Heun** - 2nd order (also Ralston)

        -   **Runge-Kutta** - 4th order (3/8-rule)

    -   **Stochastic** fixed time step:

        -   **Euler-Maruyama** - method (**Euler** also autodetects
            stochasticity)

    -   Stiff/non-stiff adaptive

        -   **Cash-Karp+Rosenbrock** (planned)

-   **time-step**:

    -   **Fixed** schemes: integration step size, given in system time.

    -   **Adaptive** schemes: Coupling interval given in system time,
        i.e. maximum step size without coupling to other (spatial)
        processes. In particular diffusion processes are coupled with an
        operator splitting scheme and rely on the given time step to get
        coupled accurately.

-   **time-scaling** (optional): scales the dynamics of the
    [System](#_group__ML__System) relative to the simulation time. The
    time within the system runs prefactored with the **time-scaling**.

**Note:** Systems define their own [Scope](#_group__Scope). This implies
that values of symbols defined within a [System](#_classSystem) are not
accessible outside of the [System](#_classSystem). Multiple Systems can
be defined within the same parental Scope, easing modular model
development.

# Time {#_group__ML__Time}

Time

Sets the duration of a simulation and controls the pseudo-random number
generator\'s seed.

**StartTime** specifies the initial time point. Default 0.

**StopTime** specifies the final time point. Must be larger than
StartTime.

**TimeSymbol** specifies a symbol to refer to the current time, e.g. in
[Event](#_group__ML__Event) conditions.

**RandomSeed** specifies a seed for the pseudo-random number generator.
A user-specified seed allows to reproduce stochastic simulation results,
including [CPM](#_group__ML__CPM). **Note:** For multithreaded
simulations, note that each thread is seeded separately based on that
user specified seed ([Parallelization](#_group__Parallelization)). This
implies that for reproducing simulations, the RandomSeed as well as the
number of parallel threads must be conserved. If **RandomSeed** is
unspecified the pseudo-random number generator will initialize based on
the system\'s time stamp and hence yields different simulation results
in subsequent runs.

**StopCondition** provides a condition to terminate the simulation. This
is handy within automated parameter exploration via parameter sweeps.

**SaveInterval** specifies the interval for checkpointing: writing the
complete simulation state to a file (xml.gz). Use the special value
\'-1\' to never save simulation state (default) or \'0\' to save state
at end of simulation (either **StopTime** or after fulfilling
**StopCondition**).

## Example {#_group__ML__Function_1Example}

    <Time>
        <StartTime value="0.0"/>
        <StopTime value="1.0"/>
        <TimeSymbol symbol="t" name="time">
        <RandomSeed value="1234"/>
        <SaveInterval value="-1"/>
        <StopCondition>
            <Condition> celltype.ct1.size == 0 </Condition>
        </StopCondition>
    </Time>

# VariableVector {#_group__ML__VariableVector}

VariableVector

Symbol with a variable 3D vector value. The **initial** value is given
by the **value** attribute as a
[MathExpressions](#_group__MathExpressions).

Syntax is comma-separated as given by **notation** :

-   orthogonal - x,y,z

-   radial - r,φ,θ

-   or radial - φ,θ,r

# Variable {#_group__ML__Variable}

Variable

Symbol with a variable scalar value. The **initial** value is given by
the **value** attribute as a
[MathExpressions](#_group__MathExpressions).

# VectorEquation {#_group__ML__VectorEquation}

VectorEquation

Assignment of mathematical expression to a vector symbol.

Syntax is comma-separated as given by **notation** :

-   orthogonal - x,y,z

-   radial - r,φ,θ

-   or radial - φ,θ,r

During simulation it is asserted that the provided relation always
holds. Therefore, the expression may not depend on the referred output
symbol. For recurrence equations, use a
[VectorRule](#_group__ML__VectorRule) within Systems.

## Examples {#_group__ML__VectorRule_1Examples}

Assign a value by comma separated list of 3 expressions.

    <VectorEquation symbol-ref="v">
        <Expression> 2*a, a+1, a+b </Expression>
    </VectorEquation>  

Normalise a Vector to length of 5 using element-wise vector calculus
(assume u is a Vector).

    <VectorEquation symbol-ref="v">
        <Expression> 5 * u / u.abs </Expression>
    </VectorEquation>  

Using spherical coordinates

    <VectorEquation symbol-ref="v" notation="r,φ,θ">
        <Expression> radius, angle_phi, angle_theta </Expression>
    </VectorEquation>

# VectorField {#_group__ML__VectorField}

VectorField

A **VectorField** defines a variable vector field, associating an
(x,y,z) value to every lattice site, and defines a **symbol** for it.
Spatio-temporal dynamics can be implemented explicitly by using a
[VectorEquation](#_group__ML__VectorEquation) or
[VectorRule](#_group__ML__VectorRule). The [Space](#_group__ML__Space)
symbol allows the initial expression to directly depend on the spatial
position.

-   **value:** **initial** condition for the vector field. May be given
    as space-dependent [MathExpressions](#_group__MathExpressions).

**BoundaryValue** defines the value of the
[VectorField](#_group__ML__VectorField) at the respective boundary,
which may depend on time and space. By default, boundary values are
constant (0,0,0), or periodic, if defined as such under
[Lattice](#_group__ML__Lattice).

# VectorFunction {#_group__ML__VectorFunction}

VectorFunction

Symbol that defines a relation between vector
[Symbols](#_group__Symbols) from the [Scope](#_group__Scope) of the
VectorFunction definition and other \*Function\*s to a scalar result.

Syntax is comma-separated as given by **notation** :

-   orthogonal - x,y,z

-   radial - r,φ,θ

-   or radial - φ,θ,r

# VectorMapper {#_group__ML__VectorMapper}

VectorMapper

Map vector data from a spatial context into another symbol, usually
reducing spatial resolution by a mapping function.

Map vector data from a spatial context into another symbol, usually
reducing spatial resolution by a mapping function.

## Description {#_group__LengthConstraint_1Description}

A **VectorMapper** defines how data within a spatial context, e.g. a
cell, a cell population or at global scope, can be mapped to a symbol
with a different spatial granularity (i.e. resolution). Note that
defining a Mapper within a [CellType](#_group__ML__CellType) also
restricts the mapping to the spatial range occupied by the respective
cell population.

A single **Input** element must be specified:

-   **value:** input variable (e.g.
    [PropertyVector](#_group__ML__PropertyVector) or
    [VectorField](#_group__ML__VectorField)) or a respective expression.

That information can be written to an output symbol, if necessary,
reduced in spatial granularity by means of the **mapping** statistics.
If the output granularity is sufficient, i.e. when writing to a
[Field](#_group__ML__Field), no **mapping** function needs to be
specified.

Multiple **Output** elements can be specified:

-   **mapping:** statistic used for data mapping (if needed)

-   **symbol-ref**: ouput symbol (referencing e.g. a
    [VariableVector](#_group__ML__VariableVector) or a
    [PropertyVector](#_group__ML__PropertyVector)

## Example {#_group__ML__Function_1Example}

Compute the average velocity of a cell population. (Assume \'vel\'
refers to a [PropertyVector](#_group__ML__PropertyVector) containing the
cell velocity ([MotilityReporter](#_group__MotilityReporter)) and
\'avg_vel\' global [VariableVector](#_group__ML__VariableVector))

    <VectorMapper>
        <Input value="vel" />
        <Output symbol-ref="avg_vel" mapping="average" />
    </VectorMapper>

# VectorRule {#_group__ML__VectorRule}

VectorRule

Assignment of mathematical expression to a symbol.

Differs from [VectorEquation](#_group__ML__VectorEquation) in that a
VectorRule:

-   may contain recurrence relations e.g. ![](form_99.png)

-   can only appear in [System](#_group__ML__System)

-   explicitly scheduled based on user-specified [System](#_classSystem)
    time-step

Syntax is comma-separated as given by **notation** : orthogonal - x,y,z
radial - r,φ,θ or radial - φ,θ,r

## Examples {#_group__ML__VectorRule_1Examples}

Assign a value by comma separated list of 3 expressions.

    <System solver="euler" time-step="1">
        <VectorRule symbol-ref="a">
            <Expression> 2*a, a+1, a+b </Expression>
        </VectorRule>  
    </System>

# VolumeConstraint {#_group__ML__VolumeConstraint}

VolumeConstraint

Penalizes deviations from target cell area (2D) or volume (3D)

Penalizes deviations from target cell area (2D) or volume (3D)

The volume constraint models the conservation of area (2D) or volume
(3D) of cells.

It puts a quadratic energy penality to deviations of the area (2D) or
volume (3D) of a cell ![](form_52.png) from a given target (resting)
area or volume ![](form_53.png) , specified in units of lattice sites.
The strength of this penalty is modulated by a Langrangian multiplier
![](form_54.png) that determines the cell\'s incompressibility.

The Hamiltonian is given by:

![](form_55.png)

For each proposed copy attempt ![](form_56.png) , the change in
effective energy is computed as:

![](form_57.png) where

-   ![](form_54.png) is a Lagrangian multiplier given the strength of
    the constraint, related to the cell\'s incompressibility

-   ![](form_58.png) is the current volume of cell ![](form_31.png) at
    time ![](form_59.png)

-   ![](form_60.png) is the projected (if updated would be accepted)
    volume of cell ![](form_31.png) at time ![](form_59.png)

-   ![](form_53.png) is the target volume of cell ![](form_31.png) at
    time ![](form_59.png)

## Input {#_group__LengthConstraint_1Input}

-   *target*: Expression describing the target area (2D) or volume (3D)
    of a cell ![](form_53.png) , in units of lattice sites. This may be
    a constant (e.g. \"100.0\"), a symbol (e.g. \"Vt\"), or an
    expression (e.g. \"V0 \* 2.0\")

-   *strength*: Expression describing the strength of the volume
    constraint ![](form_54.png) , in units of energy. This may be a
    constant (e.g. \"100.0\"), a symbol (e.g. \"S\"), or an expression
    (e.g. \"S0 \* 2.0\")

## Reference {#_group__LengthConstraint_1Reference}

-   Graner, François, and James A. Glazier. \"Simulation of biological
    cell sorting using a two-dimensional extended Potts model.\"
    Physical review letters 69:13, 1992.
    <http://dx.doi.org/10.1103/PhysRevLett.69.2013>

## Example {#_group__ML__Function_1Example}

    <VolumeConstraint strength="1" target="100"/>

    <VolumeConstraint strength="s" target="Vt"/>

    <VolumeConstraint strength="S * 2.0" target="V0 * 2.0"/>

# MorpheusML {#_group__MorpheusML}

MorpheusML

## Modules {.unnumbered}

-   [Analysis](#_group__ML__Analysis)

-   [CPM](#_group__ML__CPM)

-   [CellPopulations](#_group__ML__CellPopulations)

-   [CellTypes](#_group__ML__CellTypes)

-   [Description](#_group__Description)

-   [Global](#_group__ML__Global)

-   [ParamSweep](#_group__ParamSweep)

-   [Space](#_group__ML__Space)

-   [Time](#_group__ML__Time)

## Detailed Description

# MotilityReporter {#_group__MotilityReporter}

MotilityReporter

Reports statistics about cell motility.

Reports statistics about cell motility.

## Description {#_group__LengthConstraint_1Description}

MotilityReporter reports statistics about cell motility.

-   **Velocity:** estimates cell velocity over time intervals of length
    time-step \[simulation time units\].

-   **Displacement:** measures the displacement of a cell relative to
    it\'s original position at simulation start.

## Example {#_group__ML__Function_1Example}

Report every 10 \[simulation time units\] the velocity and displacement
of cells into properties A and B. (Assume both \'A\' and \'B\' refer to
a VectorProperty of the cell)

    <MotilityReporter time-step="10.0">
        <Velocity symbol-ref="A" />
        <Displacement symbol-ref="B" />
    </MotilityReporter>

# Evaluating math expressions {#_group__MuParser}

Evaluating math expressions

Mathematical expressions are evaluated at run-time using
[MuParser](http://beltoforion.de/article.php?a=muparser), while all
variables are resolved using Morpheus\' [Symbols](#_group__Symbols)
system. Vector expression evaluation is performed component-wise. see
[MathExpressions](#_group__MathExpressions)

# NeighborhoodReporter {#_group__NeighborhoodReporter}

NeighborhoodReporter

Reports data about a node\'s or a cell\'s neighborhood or
\'microenvironment\'.

Reports data about a node\'s or a cell\'s neighborhood or
\'microenvironment\'.

## Description {#_group__LengthConstraint_1Description}

### CellType {#_group__NeighborhoodVectorReporter_1CellType}

NeighborhoodReporter reports about the adjacent Neighborhood of a cell,
i.e. the cell\'s \'microenvironment\'. Information can be retrieved from
all contexts within the neighborhood (i.e. [Property](#_classProperty)
or [MembraneProperty](#_classMembraneProperty) of neighboring cells,
Field concentrations) and, if necessary, mapped to a scalar value within
the output context.

The neighborhood size is defined by the ShapeSurface neighborhood within
[CPM](#_group__ML__CPM) definition of (CPM/ShapeSurface/Neighborhood).

### Global {#_group__NeighborhoodVectorReporter_1Global}

NeighborhoodReporter reports about the adjacent Neighborhood of a node,
i.e. the node\'s \'microenvironment\'.

The neighorhood size is defined by the default neighborhood within the
[Lattice](#_group__ML__Lattice) definition.

## Parameters {#_group__NeighborhoodVectorReporter_1Parameters}

A single **Input** element must be specified:

-   **value:** input expression (e.g. [Property](#_classProperty),
    [MembraneProperty](#_classMembraneProperty) or Field), which is
    evaluated at global scope in the whole neighborhood. The local
    cell\'s/node\'s scope is available under namespace \'local\', e.g. a
    cell\'s own id is \'local.cell.id\' while the id of any of it\'s
    neighbors is \'cell.id\'.

-   **scaling:** setting scaling to **per_cell** will aquire information
    per neighboring cell (entity), **per_length** will scale the
    information with the interface length, i.e. the input value is
    considered to be a rate per node length.

-   **noflux-cell-medium**: if true, the cell-medium interfaces are
    treated as no-flux boundaries. That is, at these interfaces, the
    value will be taken from the cell itself instead of the (empty)
    neighborhood.

Note, accessing the local cell\'s/node\'s properties in the input
expression is directly possible through the symbol namespace \'local\'.

If input is a Vector, use
[NeighborhoodVectorReporter](#_group__NeighborhoodVectorReporter).

Several Output tags can be specified, each referring to an individual
property of the aquired information. If the information is written to a
[MembraneProperty](#_classMembraneProperty), no mapping is required,
since their granularity is sufficient.

Multiple **Output** elements can be specified:

-   **mapping:** statistic used for data mapping (if needed)

-   **symbol-ref**: ouput variable (e.g. [Property](#_classProperty) or
    [MembraneProperty](#_classMembraneProperty))

### Examples {#_group__ML__VectorRule_1Examples}

Average and Variance of a value defined by an expression in surrounding
cells (Assume \'A\' and \'B\' refer to CellProperties)

    <NeighborhoodReporter>
        <Input value="c+a+b" scaling="cell"/>
        <Output symbol-ref="A" mapping="avg" />
        <Output symbol-ref="B" mapping="var" />
    </NeighborhoodReporter>

Spatially resolved distribution of a (membrane) concentration into a
CellMembraneProperty \'B\' (Consider cMemProt to be a concentration of a
membrane Protein)

    <NeighborhoodReporter>
        <Input value="min(cMemProt,local.cMemProt)" />
        <Output symbol-ref="B" />
    </NeighborhoodReporter>

Count the number of cells of a particular celltype (ct2) in the cell\'s
neighborhood (Assume \'A\' refers to a CellProperty)

    <NeighborhoodReporter>
        <Input value="cell.type == celltype.ct2" scaling="cell"/>
        <Output symbol-ref="A" mapping="sum"/>
    </NeighborhoodReporter>

Surface length of a whole cell population (ct1) with other cells /
medium (Assume \'A\' refers to a Variable)

    <NeighborhoodReporter>
        <Input value="cell.type != celltype.ct1" scaling="length"/>
        <Output symbol-ref="A" mapping="sum"/>
    </NeighborhoodReporter>

# NeighborhoodVectorReporter {#_group__NeighborhoodVectorReporter}

NeighborhoodVectorReporter

Reports data about a node\'s or a cell\'s neighborhood or
\'microenvironment\' using Vector input.

Reports data about a node\'s or a cell\'s neighborhood or
\'microenvironment\' using Vector input.

## Description {#_group__LengthConstraint_1Description}

### CellType {#_group__NeighborhoodVectorReporter_1CellType}

NeighborhoodVectorReporter reports about the adjacent Neighborhood of a
cell, i.e. the cell\'s \'microenvironment\' using Vector input.
Information can be retrieved from all contexts within the neighborhood
and, if necessary, mapped to a scalar value within the output context.

The neighborhood size is defined by the ShapeSurface neighborhood within
[CPM](#_group__ML__CPM) definition of (CPM/ShapeSurface/Neighborhood).

### Global {#_group__NeighborhoodVectorReporter_1Global}

NeighborhoodVectorReporter reports about the adjacent Neighborhood of a
node, i.e. the node\'s \'microenvironment\' and writes it to a Field.

The neighorhood size is defined by the default neighborhood within the
[Lattice](#_group__ML__Lattice) definition.

## Parameters {#_group__NeighborhoodVectorReporter_1Parameters}

A single **Input** element must be specified:

-   **value:** input expression (e.g. VectorProperty), which is
    evaluated at global scope in the whole neighborhood. The local
    cell\'s/node\'s scope is available under namespace \'local\', e.g. a
    cell\'s own id is \'local.cell.id\' while the id of any of it\'s
    neighbors is \'cell.id\'.

-   **scaling:** setting scaling to **per_cell** will aquire information
    per neighboring cell (entity), **per_length** will scale the
    information with the interface length, i.e. the input value is
    considered to be a rate per node length.

Note, accessing the local cell\'s/node\'s properties in the input
expression is directly possible through the symbol namespace \'local\'.

If input variable is a scalar, use
[NeighborhoodReporter](#_group__NeighborhoodReporter).

Several Output tags can be specified, each referring to an individual
property of the aquired information. If the information is written to a
[MembraneProperty](#_classMembraneProperty), no mapping is required,
since their granularity is sufficient.

Multiple **Output** elements can be specified:

-   **mapping:** statistic used for data mapping (if needed)

-   **symbol-ref**: ouput variable of Vector type (e.g. VectorProperty)

## Examples {#_group__ML__VectorRule_1Examples}

(Assume \'Aa\' to represent a VectorProperty)

    <NeighborhoodVectorReporter>
        <Input value="0.1*a.x, 0.1*a.y, 0" />
        <Output symbol-ref="Aa" />
    </NeighborhoodVectorReporter>

# Parallelization {#_group__Parallelization}

Parallelization

Morpheus employs [OpenMP](https://www.openmp.org/specifications/) as the
workload-sharing construct for all formalisms (ODE/PDE/CPM/Mappers). The
parallel CPM computation makes heavy use of locking, such that
parallelization on multi-socket systems may suffer serious a performance
impact when spanning more that one socket. Consider to restrict the
number of parallel threads accordingly.

In the GUI use the **threads per job** settings and in a shell the
environment variable **\`OMP_NUM_THREADS\`** to adjust the number of
usable threads.

# ParamSweep {#_group__ParamSweep}

ParamSweep

Specification of a batch process for parameter exploration or
sensitivity analysis.

-   Parameter(s) are selected via the context menu in their respective
    model section and only selected parameters appear in the
    **ParamSweep** panel.

-   Parameter values are specified as a list or range under **Values**.

-   To change parameters consecutively instead of combinatorially,
    drag-and-drop a parameter on another.

-   Execute the batch process through the **Start** button in the
    **ParamSweep** panel. You will see a summary of the job list to be
    started.

-   Repetitions of stochastic simulations with identical parameter set
    can be generated by adding a dummy parameter and sweeping of it.

# PersistentMotion {#_group__PersistentMotion}

PersistentMotion

PersistentMotion models the tendency of cells to maintain their previous
direction of movement (memory or inertia), due to the non-instantaneous
turnover of the cytoskeleton

Cells have a target direction ![](form_34.png) based on previous
movement, and CPM update in this direction are preferred (i.e. they
decrease energy ![](form_35.png) ).

For each proposed copy attempt ![](form_29.png) in direction
![](form_36.png) , the change in effective energy is computed as:

![](form_37.png)

where

-   ![](form_25.png) is the strength of persistence, in units of energy.

-   ![](form_38.png) is the cell volume

-   ![](form_39.png) is a vector giving the target direction of previous
    movement

-   ![](form_36.png) is a vector giving the direction of CPM update

The target direction is updated continuously according to the shift of
cell centroid within a certain time window ![](form_40.png) , keeping a
memory of length \'decaytime\' ![](form_41.png) :

![](form_42.png)

## Input {#_group__LengthConstraint_1Input}

### Required {#_group__PersistentMotion_1autotoc_md9}

-   **decay-time**: Expression representing the memory of direction of
    cell movement. This may be a constant (e.g. \"50.0\"), a symbol
    (e.g. \"St\"), or an expression (e.g. \"S0 \* 2.0\")

-   **strength:** Expression describing the strength of persistence.
    This may be a constant (e.g. \"2.0\"), a symbol (e.g. \"Ss\"), or an
    expression (e.g. \"S0 \* 2.0\")

### Optional {#_group__PersistentMotion_1autotoc_md10}

-   **orientation-symbol** : Provide a cell property to store the
    current cell orientation.

-   **observation-window** (default=1): Time window for observing the
    cell\'s displacement direction. Defaults to the duration of 1 MCS.
    Note that the window size will also contribute to the cell\'s
    persistency.

-   **update-orientation** (default=**cell-mass-displacement**):
    Orientation of a cell update is either estimated through the
    displacement of it\'s center of mass (**cell-mass-displacement**),
    through the orientation from update source to target
    (**source-to-target**), or through the orientation perpendicular to
    the local cell surface (**surface-normal**).

-   **protrusions** (default=true): Boolean describing whether
    persistence should be considered during protrusions.

-   **retractions** (default=false): Boolean describing whether
    persistence should be considered during retractions.

## Notes {#_group__LengthConstraint_1Notes}

-   This plugin stores the old cell center and target direction as
    VectorProperties in the cell.

## Reference {#_group__LengthConstraint_1Reference}

-   Szabó, A., R. Ünnep, E. Méhes, W. O. Twal, W. S. Argraves, Y. Cao,
    and A. Czirók. \"Collective cell motion in endothelial monolayers.\"
    Physical biology 7, no. 4, 2010.

-   Vroomans, Renske MA, Paulien Hogeweg, and Kirsten HWJ ten Tusscher.
    \"Segment-Specific Adhesion as a Driver of Convergent Extension.\"
    PLOS Computational Biology 11, no. 2, 2015.

## Example {#_group__ML__Function_1Example}

    <PersistentMotion decay-time="50" strength="1"/>

    <PersistentMotion decay-time="dt" strength="s"/>

    <PersistentMotion decay-time="dt" strength="s" protrusion="true" retraction="true"/>

# by Interface {#_group__PluginsByInterface}

by Interface

## Modules {.unnumbered}

-   [Analysis Plugins](#_group__AnalysisPlugins)

-   [CPM Hamiltonian Plugins](#_group__CPM__EnergyPlugins)

-   [CPM Interaction Plugins](#_group__CPM__InteractionPlugins)

-   [CPM Update Listener
    Plugins](#_group__Cell__Update__ListenerPlugins)

-   [Cell Update Checker Plugins](#_group__Cell__Update__CheckerPlugins)

-   [Continuous Process Plugins](#_group__ContinuousProcessPlugins)

-   [Instantaneous Process
    Plugins](#_group__InstantaneousProcessPlugins)

-   [Population Initializer Plugins](#_group__InitializerPlugins)

-   [Reporter Plugins](#_group__ReporterPlugins)

-   [TimeStep Listener Plugins](#_group__TimeStepListenerPlugins)

## Detailed Description

# Plugin Types {#_group__Plugins}

Plugin Types

All Modules of morpheus belong to one or multiple basic plugin types
that are listed below.

## Modules {.unnumbered}

-   [Cell Motility Plugin](#_group__CellMotilityPlugins)

    Plugins that implement cell motility mechanisms.

-   [Cell Shape Plugins](#_group__CellShapePlugins)

    Plugins that alter cell shape.

-   [Interaction Plugins](#_group__InteractionPlugins)

    Plugins that determine cell interactions in terms of energies.

-   [Miscellaneous Plugins](#_group__MiscellaneousPlugins)

    Plugins for population management and auxiliary plugins.

-   [by Interface](#_group__PluginsByInterface)

## Detailed Description

All Modules of morpheus belong to one or multiple basic plugin types
that are listed below.

# Protrusion {#_group__Protrusion}

Protrusion

Energetically favors updates in region of high protusive activity
(actin-inspired)

Energetically favors updates in region of high protusive activity
(actin-inspired)

Implements the \'Act model\' (Niculescu et al, 2015) which extends the
CPM with a local feedback mechanism resulting in cell protrusions and,
as a consequence, in cell motility. The mechanism amplifies the inherent
membrane fluctuations of CPM cells in a manner depending on the size of
the fluctuations and their recent protrusive activity.

The protrusive activity is tracked by keeping an activity value for
every lattice site. The empty lattice sites that form the medium have a
zero activity value, while sites that are freshly incorporated by a cell
get the maximum activity value ( ![](form_43.png) ). The activity value
of a site decreases by one after every MCS, until it reaches zero,
creating a memory of MaxAct MCSs in which the site "remembers" that it
was active. The combination of the memory of a site u with the activity
in its neighborhood forms the basis for a local positive feedback
mechanism that biases the copy attempt from the active site u to a less
active site v.

The energy difference is calculated as follows:

![](form_44.png)

where ![](form_45.png)

with ![](form_46.png) defined as the direct 2nd order or Moore
neighborhood of ![](form_47.png) that belongs to the same cell.

-   **field** must refer to a [Field](#_group__ML__Field) that store the
    Activity values.

-   **strength** specifies the strength ![](form_48.png) of this energy
    term.

-   **maxmimum** specifies the maximum activity value ![](form_43.png) ,
    related to the length of the \'memory\'.

## Reference {#_group__LengthConstraint_1Reference}

-   I. Niculescu, J. Textor, R. de Boer, Crawling and Gliding: A
    Computational Model for Shape-Driven Cell Migration, PLoS Comp
    Biol, 2015. <http://dx.doi.org/10.1371/journal.pcbi.1004280>

## Examples {#_group__ML__VectorRule_1Examples}

Assuming a Field \'act\' exist to store the activity values:

    <Protrusion field="act" strength="80" maximum="200" />

# Reporter Plugins {#_group__ReporterPlugins}

Reporter Plugins

## Modules {.unnumbered}

-   [Mapper](#_group__ML__Mapper)

    Map data from a spatial context into another symbol, usually
    reducing spatial resolution by a mapping function.

-   [MotilityReporter](#_group__MotilityReporter)

    Reports statistics about cell motility.

-   [NeighborhoodReporter](#_group__NeighborhoodReporter)

    Reports data about a node\'s or a cell\'s neighborhood or
    \'microenvironment\'.

-   [NeighborhoodVectorReporter](#_group__NeighborhoodVectorReporter)

    Reports data about a node\'s or a cell\'s neighborhood or
    \'microenvironment\' using Vector input.

-   [VectorMapper](#_group__ML__VectorMapper)

    Map vector data from a spatial context into another symbol, usually
    reducing spatial resolution by a mapping function.

## Detailed Description

# Scheduling {#_group__Scheduling}

Scheduling

## Schedule {#_group__Scheduling_1Schedule}

Morpheus currently applies a static scheduling scheme, which means that
the schedule is constructed before the simulation starts and remains
unchanged until the end of the simulation. Numerical schemes, however,
may subdivide the stepping provided by the static scheduling, as done by
adaptive solvers and the stability criterion of fwd. euler diffusion.

The final scheme can be found in a simulation log.

In the initialization phase, all symbols are registered, the plugins and
their interdependencies are analysed and a **model graph** is
constructed. Using the model graph, a schedule is constructed along the
following guidelines.

-   **Correctness:** Update time steps must be fine-grained enough.

-   **Order:** Sequential order must obey the order in the directed
    acyclic model graph (DAG), which is constructed by opening up
    potential closed loops.

-   **Validity:** Updates must be performed frequently enough to provide
    the latest input values for other plugins.

-   **Efficiency:** Updates are not scheduled more often than the
    plugins\' output is required.

The **sequential** update scheme will look as follows:

-   **Phase** 1: [Continuous Process
    Plugins](#_group__ContinuousProcessPlugins)

    -   [Field](#_group__ML__Field) diffusion (CFL condition)

    -   [System](#_group__ML__System)

    -   [CPM](#_group__ML__CPM)

-   **Phase** 2: Sequential schemes ordered by dependencies

    -   [Reporter Plugins](#_group__ReporterPlugins)

    -   [Instantaneous Process
        Plugins](#_group__InstantaneousProcessPlugins)

-   **Phase** 3:

    -   [Analysis Plugins](#_group__AnalysisPlugins)

# Scope {#_group__Scope}

Scope

**Scopes** manage the symbols of the (nested) model sections, allow
symbol registration by model components and symbol retrieval by others.
Symbols defined in a scope are invalid outside of this scope, but
available in all sub-scopes, i.e. nested sections. This is analogous to
the local variable scoping in most programming languages. Special
reporter plugins can define additional information flow between
neighboring scopes.

The top-most scope is [Global](#_group__ML__Global). The following model
elements define their own sub-scopes:

-   [CellType](#_group__ML__CellType)

-   [System](#_group__ML__System) (including **Triggers** of
    [Event](#_group__ML__Event) and
    [CellDivision](#_group__ML__CellDivision))

-   [Function](#_group__ML__Function)

As stated above, symbols are inherited from the parental scope, but may
be overwritten, even to differ in constness and granularity (e.g.
Global/[Constant](#_group__ML__Constant) may be overwritten in a
[System](#_classSystem) by a [Variable](#_group__ML__Variable)). The
type of the symbol (scalar / vector), however, has to be conserved. In
this way, global symbols can be used as default values.

Unlike the other scopes, the [CellType](#_group__ML__CellType) scopes
also represent spatial compartments. In order to adhere to intuitive
modelling logics, we apply **spatial** **scoping**, such that symbols
defined in a [CellType](#_group__ML__CellType) scope can overwrite
parental, i.e. global, symbols in the (dynamic) spatial region the
celltype occupies. Therefore, a global symbol can be effectively
composed of a global value and celltype specific values defined within
the celltypes themselves. Determining the value of a composite symbol at
a specific position through the Cell/CellType occupancy of a specific
position is what we call **spatial scoping**.

When a symbol is declared in **all** CellType scopes (e.g. in all
CellTypes), it also becomes available in the global scope (known as a
virtual composite symbol).

## Examples {#_group__ML__VectorRule_1Examples}

In the following example, \'a=1\' is declared in the Global scope, and
\'b=2\' is declared in the [System](#_classSystem) scope. The global
variable \'result\' will yield \'3\'.

    <Global>
        <Constant symbol="a" value="1"/>
        <Variable symbol="result" value="0"/>

        <System solver="Euler [fixed, O(1)]" time-step="1.0">
            <Constant symbol="b" value="2"/>
            <Rule symbol-ref="result">
                <Expression>a+b</Expression>
            </Rule>
        </System>
    </Global>

  --
  --

In the following, the global constant \'a=1\' is overwritten in
[System](#_classSystem) by the local constant \'a=2\', such that
\'result\' will yield \'4\'.

    <Global>
        <Constant symbol="a" value="1"/>
        <Variable symbol="result" value="0"/>

        <System solver="Euler [fixed, O(1)]" time-step="1.0">
            <Constant symbol="a" value="2"/>
            <Constant symbol="b" value="2"/>
            <Rule symbol-ref="result">
                <Expression>a+b</Expression>
            </Rule>
        </System>
    </Global>

  --
  --

Symbols can be re-used within different local scopes. Here, the symbol
\'p\' is used in different CellTypes. In \'ct1\', \'p\' is a constant
with value \'0\'. In \'ct2\', \'p\' is a constant with value \'1.0\'. In
\'ct3\', \'p\' denote a cell-bound [Property](#_classProperty) and in
\'ct4\' it represents a [MembraneProperty](#_classMembraneProperty).

Because \'p\' is defined in all CellTypes, it is automatically also
available in the Global scope, e.g. for plotting domain-wide spatial
maps.

    <CellTypes>
        <CellType class="biological" name="ct1">
            <Constant symbol="p" value="0"/>
        </CellType>
        <CellType class="biological" name="ct2">
            <Constant symbol="p" value="1.0"/>
        </CellType>
        <CellType class="biological" name="ct3">
            <Property symbol="p" value="1"/>
        </CellType>
        <CellType class="biological" name="ct4">
            <MembraneProperty symbol="p" value="l.x / size.x">
                <Diffusion rate="0.0"/>
            </MembraneProperty>
        </CellType>
    </CellTypes>

# SurfaceConstraint {#_group__SurfaceConstraint}

SurfaceConstraint

Penalizes deviations from target cell perimeter (2D) or surface area
(3D)

Penalizes deviations from target cell perimeter (2D) or surface area
(3D)

The surface constraint penalizes deviations of the cell perimeter (2D)
or surface area ![](form_61.png) from a given target ![](form_62.png) .

This models the cell cortex rigidity by specifying the ratio between a
cell\'s surface area to its volume (or ratio between perimeter length to
area in 2D).

The target can be defined explicitly in **surface** mode, or implicitely
in **aspherity** mode as a multiple of the surface of a sphere of equal
volume.

In **surface** mode the units of the perimeter estimate are defined in
the [ShapeSurface](#_group__ML__ShapeSurface) (either node length,
neighborhood nodes or neighborhood fraction). In **aspherity** mode
target and perimeter estimate are determined in node length.

The Hamiltonian is given by ![](form_63.png)

For each proposed copy attempt ![](form_56.png) , the change in
effective energy is computed as:

![](form_64.png)

where

-   ![](form_65.png) is strength of the constraint

-   ![](form_66.png) is the current surface area of cell
    ![](form_31.png) .

-   ![](form_67.png) is the projected surface area of cell
    ![](form_31.png) (if updated would be accepted).

-   ![](form_68.png) is the target surface area of cell ![](form_31.png)
    .

-   ![](form_69.png) is the exponent.

## Input {#_group__LengthConstraint_1Input}

### Required {#_group__SurfaceConstraint_1autotoc_md13}

-   *mode*: Selects the *target* to be either

    -   **surface** : The length/surface ![](form_62.png) in
        \[node\]/\[node²\]

    -   **aspherity** : 2D: The Multiple of the perimeter of a circle of
        the same area as the cell σ, i.e. ![](form_70.png) 3D: Multiple
        of the surface of a sphere of the same volume as the cell σ,
        i.e. ![](form_71.png)

-   *target*: Expression describing the target perimeter (2D) or surface
    area (3D) of a cell.

-   *strength*: Expression describing the strength of the surface
    constraint.

### Optional {#_group__SurfaceConstraint_1autotoc_md14}

-   *exponent*: Value giving the exponents ![](form_69.png) (default:
    ![](form_72.png) ).

## Reference {#_group__LengthConstraint_1Reference}

-   Noriyuki Bob Ouchi, James A. Glazier, Jean-Paul Rieu, Arpita
    Upadhyayad, Yasuji Sawadae, Improving the realism of the cellular
    Potts model in simulations of biological cells. Physica A,
    329:451--458, 2003.

## Example {#_group__ML__Function_1Example}

# SurfaceMotion {#_group__SurfaceMotion}

SurfaceMotion

## SurfaceMotion {#_group__SurfaceMotion_1SurfaceMotion}

For each proposed copy attempt ![](form_29.png) a cell is either
extended or retracted, and depending on the local activity
![](form_49.png) and strengh ![](form_50.png) the change in effective
energy is computed as:

![](form_51.png)

The direction may be provided through a fixed value or via a cell
property.

## Input {#_group__LengthConstraint_1Input}

### Required {#_group__SurfaceMotion_1autotoc_md11}

-   *activity*: Local surface activity: \>0 prefers protrusions; \<0
    prefers retractions.

-   \*strength\*: Expression describing the strength of the bias.

### Optional {#_group__SurfaceMotion_1autotoc_md12}

-   \*protrusions\* (default=true)

-   \*retractions\* (default=true)

## References {#_group__ConnectivityConstraint_1References}

## Example {#_group__ML__Function_1Example}

    <SurfaceMotion activity="a" strength="s" [ protrusions="true" | retractions="true" ] />

# Symbols {#_group__Symbols}

Symbols

## Modules {.unnumbered}

-   [Constant](#_group__ML__Constant)

-   [ConstantVector](#_group__ML__ConstantVector)

-   [DelayProperty](#_group__ML__DelayProperty)

-   [DelayVariable](#_group__ML__DelayVariable)

-   [Field](#_group__ML__Field)

-   [Function](#_group__ML__Function)

    Parametric Function declaration.

-   [MembraneProperty](#_group__ML__MembraneProperty)

-   [Property](#_group__ML__Property)

-   [PropertyVector](#_group__ML__PropertyVector)

-   [Variable](#_group__ML__Variable)

-   [VariableVector](#_group__ML__VariableVector)

-   [VectorField](#_group__ML__VectorField)

-   [VectorFunction](#_group__ML__VectorFunction)

## Detailed Description

**Symbols** represent data sources that may vary in time, space.

Valid symbol identifiers may contain the following characters

-   Latin chars: abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ

-   Greek chars: αβγδεζηθικλμνξοπρσςτυφχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ

-   Numbers: 0123456789

-   Special chars: .\_

but must not start with a number.

The **name** attribute is used for descriptive purposes only. In
particular, graph labels will display this information. You may use
latex style super- and subscripts (c\_{1})\^{2} will become
![](form_0.png)

# Tagging {#_group__Tagging}

Tagging

Model components may be tagged by a set of comma-separated custom tags.
Tagging has no effect on the model itself but rather allows to group
components logically.

    <Field tags="chemotaxis, phase::liquid" symbol="f" />

The graphical user interface supports filtering the model views by a
subgroup of given tags. Any component that has no tag defined is
referred to by the logical group **#untagged**.

# TiffPlotter {#_group__TiffPlotter}

TiffPlotter

Writes cells and fields to multipage TIFF images.

Writes cells and fields to multipage TIFF images.

TiffPlotter can write 5D data to file in multistack multichannel TIFF
format.

Writes grayscale TIFF file in 8, 16 or 32bit format.

Multipage images are exported in XYCZT format.

TiffPlotter supports:

-   z-stack 3d images

-   multiple channels, see Channel

-   4D+time: with \'timelapse\' true, appends image to existing TIFF,
    see timeslapse

-   cropping to specific cell(s), see CropToCell

-   OME headers allow BioFormat stack support
    (ImageJ-\>Import-\>BioFormat)

Note: cannot handle hexagonal latices.

-   **format** (default=guess): bitformat of TIFF image: 8 bit (int
    0-255), 16 bit (int 0-65536), or 32 bit (float, single precision).

-   **compression** (default=true): use lossless LZW compression.

-   **timelapse** (default=true): append images to create 2D+time or
    3D+time image

-   **OME-header** (default=false): write OME-TIFF header with meta-data
    on TIFF organization (OME=Open Microscopy Environment).

-   **Channel:** defines a symbol to plot in channel, multiple channel
    are possible

    -   **symbol-ref**: Symbol to plot

    -   **celltype** (optional): To plot symbol from single cell type
        (in case of symbol-ref refers to cell
        [Property](#_classProperty)). If not defined, global scope is
        assumed.

    -   **minimum** (optional): User-specified fixed minimum value. If
        not given, determined by data.

    -   **maximum** (optional): User-specified fixed minimum value. If
        not given, determined by data.

    -   **scale** (optional): If true, data is scaled according to
        min/max values. If false, raw values are used.

    -   **outline** (default=false): Plot values on cell surface only
        (e.g. like membraneproperties are drawn). Can be used to
        visualize cells semi-transparently.

    -   **no-outline** (default=false): Do NOT plot values on cell
        surface. Can be used to separate cells in the image.

    -   **exclude-medium** (optional): Medium is not plotted (zero).

-   **CropToCell:** plot small TIFF image(s) containing single cell(s)

    -   **padding** (optional): number of voxels to add to image around
        cell volume

    -   **cell-ids** (required): list of cell IDs to plot in the
        following format: comma-separated: 1,2,3,4,5 dash-seperated: 1-5
        combined: 1,3-5

## Examples {#_group__ML__VectorRule_1Examples}

Write multiple timelapse multichannel images of cell properties
\'cell.id\' and \'c\' to 8-bit TIFF image files for cellsa with IDs
between 10 and 15.

    <TiffPlotter format="8bit" time-step="100">
        <Channel symbol-ref="cell.id" celltype="cell"/>
        <Channel symbol-ref="c" celltype="cell"/>
        <CropToCell cell-ids="10-15" padding="2"/>
    </TiffPlotter>

Write time-lapse multichannel image to 32-bit TIFF image file. See
ExcitableMedium_3D example.

    <TiffPlotter timelapse="true" format="32bit" compression="true" time-step="0.5">
        <Channel symbol-ref="u"/>
        <Channel symbol-ref="v"/>
    </TiffPlotter>

# TIFFReader {#_group__TIFFReader}

TIFFReader

## Description {#_group__LengthConstraint_1Description}

TIFFReader loads a configuration of a cell population or gradient field
from a TIFF image file.

### Cell populations {#_group__TIFFReader_1autotoc_md2}

For cell populations, a cell will be created for every unique value in
the image such that each pixel/voxel with a specific value is be part of
a unique cell.

If keepIDs=true, the cell IDs will be equivalent to the image value.

### Fields {#_group__TIFFReader_1autotoc_md3}

For gradient fields, image values correspond to concentrations.

-   From 64 bit images, double precision values are used directly and
    may be scaled by scaleToMax.

-   From 32 bit images, floating point values are used directly and may
    be scaled by scaleToMax.

-   From 16 bit images, uint16 values are divided by ![](form_11.png) ,
    and may be scaled by scaleToMax.

-   From 8 bit images, uint8 values are divided by ![](form_12.png) ,
    and may be scaled by scaleToMax.

## Notes {#_group__LengthConstraint_1Notes}

-   Multipage TIFF images (stacks) are supported.

-   LZW compressed TIFF files are supported.

-   TIFF image must have 8 (uint8), 16 (uint16), 32 (float), 64 (double)
    bit format.

-   TIFF image should be grey scale (color coded). Otherwise libTIFF
    will yield error \'\'.

## Input {#_group__LengthConstraint_1Input}

### Required {#_group__TIFFReader_1autotoc_md4}

-   *filename*: Path (string) to TIFF file.

### Optional {#_group__TIFFReader_1autotoc_md5}

-   *offset* (default=centering): X,Y,Z Coordinates to shift TIFF image
    with respect to simulation lattice. By default the offset centers
    the image if smaller than the lattice size.

-   *keepIDs* (default=\"false\"): Boolean specifying whether to keep
    the cell IDs as given in TIFF image (only relevant for loading
    CellPopulations)

-   *scaling* (default=\"1.0\"): Decimal specifying how to scale the
    values in TIFF to gradient Field (only relavant for loading Fields).

## Reference {#_group__LengthConstraint_1Reference}

N.A.

## Examples {#_group__ML__VectorRule_1Examples}

    <TIFFReader filename="image.tif" />

loading an image with an offset

    <TIFFReader filename="/home/user/path/image.tif" offset="10 10 0" />

loading a CellPopulation with offset

    <TIFFReader filename="image.tif" keepIDs="true" />

loading a Field and scaling the concentrations by factor 100

    <TIFFReader filename="image.tif" scaling="100.0" />

# TimeStep Listener Plugins {#_group__TimeStepListenerPlugins}

TimeStep Listener Plugins

# VtkPlotter {#_group__VtkPlotter}

VtkPlotter

Writes cells and fields to legacy VTK files.

Writes cells and fields to legacy VTK files.

Writes cells and fields to legacy VTK files. Currently, only ASCII
format is supported and no compression is applied.

Note: cannot handle hexagonal latices.

-   **time-step**: Time interval between saving simulation state to VTK
    file.

-   **mode** (default=binary): Write Vtk files in ascii or binary form.
    Using binary is faster and results in smaller files.

-   **Channel:** defines a symbol to plot in channel, multiple channel
    are possible

    -   **symbol-ref**: Symbol to plot

    -   **celltype** (optional): To plot symbol from single cell type
        (in case of symbol-ref refers to cell
        [Property](#_classProperty)). If not defined, global scope is
        assumed.

    -   **outline** (default=false): Plot values on cell surface only
        (e.g. like membraneproperties are drawn). Can be used to
        visualize cells semi-transparently.

    -   **no-outline** (default=false): Do NOT plot values on cell
        surface. Can be used to separate cells in the image.

    -   **exclude-medium** (optional): Medium is not plotted (zero).

## Examples {#_group__ML__VectorRule_1Examples}

    <VtkPlotter time-step="100">
        <Channel symbol-ref="cell.id"/>
        <Channel symbol-ref="act"/>
    </VtkPlotter >
# Analysis Plugins {#_group__AnalysisPlugins}

Analysis Plugins

## Modules {.unnumbered}

-   [CellTracker](#_group__CellTracker)

    Writes cell tracks in XML format.

-   [ClusteringTracker](#_group__ML__ClusteringTracker)

    Identifies and writes distribution of cell clusters within a single
    celltype.

-   [DisplacementTracker](#_group__ML__DisplacementTracker)

    Track the cell displacement of a population.

-   [External](#_group__ML__External)

    Execute external shell script.

-   [Gnuplotter](#_group__Gnuplotter)

    Visualisation of spatial simulation states (cells, fields) using
    GnuPlot.

-   [HistogramLogger](#_group__ML__HistogramLogger)

    Computation of frequency distributions and visualisation of
    histograms.

-   [Logger](#_group__Logger)

    Writes output to text file. Optionally, plots graphs.

-   [TiffPlotter](#_group__TiffPlotter)

    Writes cells and fields to multipage TIFF images.

-   [VtkPlotter](#_group__VtkPlotter)

    Writes cells and fields to legacy VTK files.

## Detailed Description

# CellDeath {#_group__CellDeath}

CellDeath

Remove cell based on a condition.

Remove cell based on a condition.

Induces cell removal upon a predefined condition.

-   **Condition:** Expression describing the condition under which a
    cell will be removed.

-   **Shrinkage:** If *no shrinkage* is specified, the cell will removed
    immediately upon fulfilling of the specified condition, modeling
    lysis. If *shrinkage is defined*, the symbol specified by
    **target-volume** is set to zero upon fulfilling of the specified
    condition. The cell is then removed if it eventually reaches
    **remove-volume**.

    -   **target_volume:** Symbol referring to the target volume as used
        in [VolumeConstraint](#_group__ML__VolumeConstraint) .

    -   **remove-volume**: cell area (2D) or volume (3D) at which the
        cell is removed

    -   **replace-with**: Rules how to replace the cell\'s volume left
        at death. The remaining nodes are replaced with either
        **medium**, the neighbor with the longest interface, or a random
        neighbor. For random neighbors, all neighbors may have the same
        probability, or the probabilities are scaled to the interfaces.

-   **Logging** (optional): Log all triggered cell death events to file,
    including all symbols defined under this tag.

## Example {#_group__ML__Function_1Example}

Stochastically removing cells through lysis (immediate removal).

    <CellDeath>
        <Condition>rand_uni(0,1) < p_death</Condition>
    </CellDeath>

Stochastically removing cells through shrinkage (removal after cell has
shrunk to volume = 3).

     <CellDeath>
        <Condition>rand_uni(0,1) < p_death</Condition>
        <Shrinkage target-volume="Vt"/>
    </CellDeath>

Stochastically removing cells through shrinkage and replacing the
remaining pixel with a random neighbor

    <CellDeath>
      <Condition>rand_uni(0,1) < p_death</Condition>
      <Shrinkage remove-volume="1" target-volume="target_volume" replace-with="random neighbor"/>
    </CellDeath>

# Cell Motility Plugin {#_group__CellMotilityPlugins}

Cell Motility Plugin

Plugins that implement cell motility mechanisms.

## Modules {.unnumbered}

-   [Chemotaxis](#_group__Chemotaxis)

    Energetically favors updates in direction of increasing
    concentration in [Field](#_group__ML__Field).

-   [DirectedMotion](#_group__DirectedMotion)

-   [FreezeMotion](#_group__FreezeMotion)

-   [Haptotaxis](#_group__Haptotaxis)

-   [Protrusion](#_group__Protrusion)

    Energetically favors updates in region of high protusive activity
    (actin-inspired)

-   [SurfaceMotion](#_group__SurfaceMotion)

## Detailed Description

Plugins that implement cell motility mechanisms.

# Cell Shape Plugins {#_group__CellShapePlugins}

Cell Shape Plugins

Plugins that alter cell shape.

## Modules {.unnumbered}

-   [ConnectivityConstraint](#_group__ConnectivityConstraint)

    Ensures cells remain connected components.

-   [InterfaceConstraint](#_group__InterfaceConstraint)

    Penalizes deviations from target cell interface length (2D) or
    interface area (3D) with cells of another cell type.

-   [LengthConstraint](#_group__LengthConstraint)

    Penalizes deviations from target cell length.

-   [SurfaceConstraint](#_group__SurfaceConstraint)

    Penalizes deviations from target cell perimeter (2D) or surface area
    (3D)

-   [VolumeConstraint](#_group__ML__VolumeConstraint)

    Penalizes deviations from target cell area (2D) or volume (3D)

## Detailed Description

Plugins that alter cell shape.

# CellTracker {#_group__CellTracker}

CellTracker

Writes cell tracks in XML format.

Writes cell tracks in XML format.

## Description {#_group__LengthConstraint_1Description}

Writes cell tracks in XML format, as used in ISBI 2012 Particle Tracking
Challenge.

These XML files can be read using the Icy plugin \"ISBI Challenge Tracks
Importer\" (which requires the Icy \"TrackManager\" plugin).
Subsequently, the cell tracks can be compared to results from automatic
cell tracking algorithms using the Icy plugin \"Tracking Performance
Measures\".

-   **time-step**: interval in which cell positions are recorded.

Note: The XML file is only written at the END of simulation (as
specified in Time/StopTime).

## Reference {#_group__LengthConstraint_1Reference}

-   Chenouard et al., Objective comparison of particle tracking methods,
    Nature Methods, 2014. <http://dx.doi.org/10.1038/nmeth.2808>

## Links {#_group__CellTracker_1Links}

-   Icy platform for bioimage informatics:
    <http://icy.bioimageanalysis.org>

-   Icy plugin \"ISBI Challenge Tracks Importer\":
    <http://icy.bioimageanalysis.org/plugin/ISBI_Challenge_Tracks_Importer>

-   Icy plugin \"Tracking Performance Measures\":
    <http://icy.bioimageanalysis.org/plugin/Tracking_Performance_Measures>

-   Description of Performance Measure:
    <http://bioimageanalysis.org/track/PerformanceMeasures.pdf>

## Example {#_group__ML__Function_1Example}

Write cell tracks to XML file, using intervals of 50 time-steps.

    <CellTracker time-step="50">
    </CellTracker>

Note: The XML file is only written at the END of simulation (as
specified in Time/StopTime).

# Cell Update Checker Plugins {#_group__Cell__Update__CheckerPlugins}

Cell Update Checker Plugins

## Modules {.unnumbered}

-   [ConnectivityConstraint](#_group__ConnectivityConstraint)

    Ensures cells remain connected components.

-   [FreezeMotion](#_group__FreezeMotion)

## Detailed Description

[Plugin](#_classPlugin) interface for defining a rule to check a cell
update before it take place. E.g. CPM\'s connectivity constraint is
based on the refusing cell updates disrupting a cell.

# CPM Update Listener Plugins {#_group__Cell__Update__ListenerPlugins}

CPM Update Listener Plugins

## Modules {.unnumbered}

-   [Protrusion](#_group__Protrusion)

    Energetically favors updates in region of high protusive activity
    (actin-inspired)

## Detailed Description

[Plugin](#_classPlugin) interface for getting notifications of cell
updates check rule for the CPM.

# ChangeCellType {#_group__ChangeCellType}

ChangeCellType

Conditionally alters CellType of cell.

Conditionally alters CellType of cell.

ChangeCelltype alters the CellType of a cell upon a condition.

-   **newCellType:** [CellType](#_group__ML__CellType) to change to
    after condition is satisfied.

-   **time-step** \[optional\]: The time step adjusts by default to 1
    Monte Carlo step (MCS) of the CPM. The time step be overridden by
    setting the **time-step** attribute.

-   **Condition:** expression that triggers the celltype change.

-   **Tiggers:** (optional): a [System](#_classSystem) of Rules that are
    triggered for both daughter cells after cell division.

-   **Logging** (optional): Log all triggered cell type change events to
    file, including all symbols defined under this tag.

## Example {#_group__ML__Function_1Example}

    <ChangeCellType newCellType="ct_differentiated_A" time-step>
        <Condition> 
            cell_fate_morphogen_A >= 1
        </Condition>
    <ChangeCellType>

# Chemotaxis {#_group__Chemotaxis}

Chemotaxis

Energetically favors updates in direction of increasing concentration in
[Field](#_group__ML__Field).

Energetically favors updates in direction of increasing concentration in
[Field](#_group__ML__Field).

## Description {#_group__LengthConstraint_1Description}

Modifies effective energy ![](form_21.png) to favor updates in the
direction of increasing concentration of a gradient field.

In the simplest case (Savill and Hogeweg, 1997): ![](form_22.png)

where

-   ![](form_23.png) is the concentration of field ![](form_1.png) at
    position ![](form_24.png)

-   ![](form_25.png) is the chemotactic strength

### Chemotaxis with saturation {#_group__Chemotaxis_1autotoc_md6}

When saturation is specified, the following generalized formula is used:

![](form_26.png)

where ![](form_27.png) is the saturation constant, which may be constant
or cell- or location specific.

-   **field:** Expression describing gradient. This may be a symbol
    representing a field (e.g. \"c\", or an expression describing a
    gradient (e.g. \"l.x / size.x\").

-   **strength:** Expression describing chemotactic strength.

-   **update-orintation** (default=`cell-mass-displacement`):
    Orientation of a cell update is either estimated through the
    displacement of it\'s center of mass (`cell-mass-displacement`),
    through the orientation from update source to target
    (`source-to-target`), or through the orientation perpendicular to
    the local cell surface (`surface-normal`).

-   **saturation** (default=None): Symbol representing the saturation
    constant (may refer to cell [Property](#_classProperty) or
    [MembraneProperty](#_classMembraneProperty))

-   **protrusion** (default=true): Boolean describing whether
    protrusions should be considered.

-   **retraction** (default=True): Boolean describing whether
    retractions should be considered.

-   **contact_inhibition** (default=False): If true, only
    protusions/retractions to/from medium yield nonzero energy.

## Reference {#_group__LengthConstraint_1Reference}

-   Savill NJ, Hogeweg P. Modelling morphogenesis: from single cells to
    crawling slugs. J Theor Biol. 1997;184:229--235.

-   Merks, Roeland MH, Erica D. Perryn, Abbas Shirinifard, and James A.
    Glazier. \"Contact-inhibited chemotaxis in de novo and sprouting
    blood-vessel growth.\" PLoS computational biology 4, no. 9 (2008):
    e1000163.

## Examples {#_group__ML__VectorRule_1Examples}

    <Chemotaxis field="c" strength="1">
    </Chemotaxis>

# Concepts {#_group__Concepts}

Concepts

## Modules {.unnumbered}

-   [Evaluating math expressions](#_group__MuParser)

-   [Parallelization](#_group__Parallelization)

-   [Scheduling](#_group__Scheduling)

-   [Scope](#_group__Scope)

-   [Tagging](#_group__Tagging)

## Detailed Description

# ConnectivityConstraint {#_group__ConnectivityConstraint}

ConnectivityConstraint

Ensures cells remain connected components.

Ensures cells remain connected components.

Prevents updates that disrupt connectivity of cell domains. I.e. ensures
that cells remain connected components.

## Note {#_group__ConnectivityConstraint_1Note}

Currently the algorithm exclusively works in 2D lattices.

## References {#_group__ConnectivityConstraint_1References}

-   Merks, Roeland MH, Sergey V. Brodsky, Michael S. Goligorksy,
    Stuart A. Newman, and James A. Glazier. \"Cell elongation is key to
    in silico replication of in vitro vasculogenesis and subsequent
    remodeling.\" Developmental biology 289, no. 1 (2006): 44-54.

## Example {#_group__ML__Function_1Example}

    <Connectivity />

# ContactLogger {#_group__ContactLogger}

ContactLogger

Write the contacts and contact lengths between cells to file.

Write the contacts and contact lengths between cells to file.

## Description {#_group__LengthConstraint_1Description}

ContactLogger write the cell-cell contacts, their contact lengths/areas
and, optionally their duration, to file.

If no celltypes are specified, reports on cell-cell contacts between all
celltypes. This includes the medium if ignore-medium is false.

## Input {#_group__LengthConstraint_1Input}

-   **celltype-from**: Only report on contacts of cells of this
    celltype.

-   **celltype-to**: Only report on contacts between this celltype and
    celltype-from (requires specification of celltype-from).

-   **ignore-medium**: Do not report on contact to medium
    (default=true).

-   **log-duration**: Report on the duration (in time) of each cell-cell
    contact. Note that keeping track of this contact duration invokes a
    computational penalty.

## Examples {#_group__ML__VectorRule_1Examples}

Periodically write all contact length of cell-cell contacts between all
cell types (excluding medium)

    <ContactLogger time-step="100"/>

Log all contacts of ct1 (including medium)

    <ContactLogger time-step="100" celltype-from="ct1" ignore-medium="false"/>

Log all contacts between ct1 and ct2 (ignoring medium)

    <ContactLogger time-step="100" celltype-from="ct1" celltype-to="ct2" log-duration="true"/>

# Continuous Process Plugins {#_group__ContinuousProcessPlugins}

Continuous Process Plugins

## Modules {.unnumbered}

-   [CPM](#_group__ML__CPM)

-   [System](#_group__ML__System)

## Detailed Description

# CPM Hamiltonian Plugins {#_group__CPM__EnergyPlugins}

CPM Hamiltonian Plugins

## Modules {.unnumbered}

-   [Chemotaxis](#_group__Chemotaxis)

    Energetically favors updates in direction of increasing
    concentration in [Field](#_group__ML__Field).

-   [DirectedMotion](#_group__DirectedMotion)

-   [Haptotaxis](#_group__Haptotaxis)

-   [InterfaceConstraint](#_group__InterfaceConstraint)

    Penalizes deviations from target cell interface length (2D) or
    interface area (3D) with cells of another cell type.

-   [LengthConstraint](#_group__LengthConstraint)

    Penalizes deviations from target cell length.

-   [MechanicalLink](#_group__ML__MechanicalLink)

-   [PersistentMotion](#_group__PersistentMotion)

-   [Protrusion](#_group__Protrusion)

    Energetically favors updates in region of high protusive activity
    (actin-inspired)

-   [SurfaceConstraint](#_group__SurfaceConstraint)

    Penalizes deviations from target cell perimeter (2D) or surface area
    (3D)

-   [SurfaceMotion](#_group__SurfaceMotion)

-   [VolumeConstraint](#_group__ML__VolumeConstraint)

    Penalizes deviations from target cell area (2D) or volume (3D)

## Detailed Description

# CPM Interaction Plugins {#_group__CPM__InteractionPlugins}

CPM Interaction Plugins

## Modules {.unnumbered}

-   [AddOnAdhesion](#_group__ML__AddOnAdhesion)

    Additive interaction energy based on a global expression
    (deprecated)

-   [HeterophilicAdhesion](#_group__ML__HeterophilicAdhesion)

    Heterophilic adhesive interaction between neighboring CPM cells.

-   [HomophilicAdhesion](#_group__ML__HomophilicAdhesion)

    Homophilic adhesive interaction between neighboring CPM cells.

## Detailed Description

# CSVReader {#_group__CSVReader}

CSVReader

Initializes cell population from CSV file.

Initializes cell population from CSV file.

## Description {#_group__LengthConstraint_1Description}

CSVReader loads a cell configuration for a population from a CSV file.
Cells are seeded with a single node, and will reach their target volume
during simulation. Format is as follows:

    \<cell name\>,\<pos.x\>,\<pos.y\>{,\<pos.z\>}
    ...

where the z-position defaults to 0.

-   **filename** denotes the csv file

-   **scaling** allows to scale the configuration defined in the csv

## Example {#_group__ML__Function_1Example}

    <CSVReader filename="cellpop1.csv" scaling="2,2,2" />

# Description {#_group__Description}

Description

**Description** provides a human readable title and annotation.

**Title** (required): name of the simulation model. This is used as
folder name to store simulation results, appended by the job ID.

**Details** (optional): human readable model annotations in plain text.
This may include a verbal model description, change history or
references. This data only serves as information for users and does not
affect the simulation itself.

## Example {#_group__ML__Function_1Example}

    <Description>
        <Title>Your Model Name</Title>
        <Details>Your annotations, change log and references.</Details>
    </Description>

# DirectedMotion {#_group__DirectedMotion}

DirectedMotion

## Description {#_group__LengthConstraint_1Description}

Directed Motion puts an energetic bias for a cell in a given direction
![](form_28.png) .

For each proposed copy attempt ![](form_29.png) and the thereby induced
displacement ![](form_30.png) of cell ![](form_31.png) , the change in
effective energy is computed as:

![](form_32.png) ,

where ![](form_33.png) denotes the cells volume, i.e. the volume
translated by ![](form_30.png) .

The direction may be provided through a fixed value or via a cell
property.

## Input {#_group__LengthConstraint_1Input}

### Required {#_group__DirectedMotion_1autotoc_md7}

-   **direction:** Symbol representing vector (property or function).

-   **strength:** Expression describing the strength of the bias. This
    may be a constant (e.g. \"2.0\"), a symbol (e.g. \"s\"), or an
    expression (e.g. \"s0 \* 2.0\")

### Optional {#_group__DirectedMotion_1autotoc_md8}

-   **update-orientation** (default=**cell-mass-displacement**):
    Orientation of a cell update is either estimated through the
    displacement of it\'s center of mass (**cell-mass-displacement**),
    through the orientation from update source to target
    (**source-to-target**), or through the orientation perpendicular to
    the local cell surface (**surface-normal**).

-   **protrusion** (default=true)

-   **retraction** (default=true)

## References {#_group__ConnectivityConstraint_1References}

## Example {#_group__ML__Function_1Example}

    <DirectedMotion direction="d" strength="s" [ protrusions="true" | retractions="true" ] />

# FreezeMotion {#_group__FreezeMotion}

FreezeMotion

FreezeMotion conditionally prevents all CPM updates, rendering a cell
immotile.

## Input {#_group__LengthConstraint_1Input}

-   *condition*: Expression describing condition under which cell become
    immotile. True if expression \>= 1.0.

## Examples {#_group__ML__VectorRule_1Examples}

Prevent all motility of cells in the cell type

    <FreezeMotion condition="1" />

Prevent motility of cells larger than 100 nodes.

    <FreezeMotion condition="cell.volume > 100" />

Prevent motility after a certain time. Assumes SymbolTime is \'time\'.

    <FreezeMotion condition="time > 100" />

# Gnuplotter {#_group__Gnuplotter}

Gnuplotter

Visualisation of spatial simulation states (cells, fields) using
GnuPlot.

Visualisation of spatial simulation states (cells, fields) using
GnuPlot.

## Description {#_group__LengthConstraint_1Description}

Gnuplotter plots the Cell configurations (and optionally Fields) to
screen or to file during simulation. Requires GNUPlot 4.2.5 or higher.

Organized in Plots, several artistic representations can be selected:

-   Cells can be colorized using the value attribute.

-   Spatial Fields can be superimposed under the plot.

-   Additional information can be visualized using CellLabels and
    CellArrows.

-   VectorFields can be plotted by providing x and y components
    separately.

### Attributes {#_group__Gnuplotter_1Attributes}

-   **time-step** (optional): Frequency of plotting events. If
    unspecified, adopts to the frequency of input updates. Setting
    **time-step=0** will plot only the final state of the simulation.

-   **decorate** (optional, true): Enables axis labels and legends.

-   **log-commands** (optional, false): Enables logging of data and
    plotting commands to disc. Allows to manually repeat and manipulate
    the plots.

-   **file-numbering** (optional, time): Set the numbering of the plot
    images to either be consecutive or based on simulation time.

-   **condition** (optional, 1): A condition that will skips plotting if
    the condition is evaluated to 0.

### Terminal {#_group__Gnuplotter_1Terminal}

-   **name:** Specifies the output format (e.g. wxt, x11, aqua, png,
    postscript). Default is Gnuplot default.

### Plot {#_group__Logger_1Plot}

-   **title:** Title of the plot.

-   **slice:** Z-slice of 3D lattice to plot.

-   **Cells:** Plot the spatial cell pattern restricted to a 2d
    scenario. Cell coloring is determined by the **value** attribute.

-   **CellLabels:** Put labels at the cell center according to the
    expression provided with the **value** attribute.

-   **CellArrows:** Put arrows at the cell center according to the
    expression provided with the **value** attribute.

-   **CellLinks:** Put a line connecting cell centers for each link
    created by [MechanicalLink](#_group__ML__MechanicalLink) component.

-   **Field:** Plot a scalar field given by the expression in **value**.
    **Coarsening** will reduce the spatial data resolution.

-   **VectorField:** Plot a vector field given by the expression in
    **value**. **Coarsening** will reduce the spatial data resolution.

## Examples {#_group__ML__VectorRule_1Examples}

Plot CPM state (showing cell types) to screen using WxWidgets terminal

    <Analysis>
            <Gnuplotter time-step="100">
                <Terminal name="png"/>
                <Plot>
                    <Cells value="cell.id" />
                </Plot>
            </Gnuplotter>
    <\Analysis>

Example: Plot CPM state showing two cell properties to PNG files

    <Analysis>
            <Gnuplotter time-step="100">
                <Terminal name="png"/>
                 <Plot>
                    <Cells value="cell.volume.target" />
                 </Plot>
                 <Plot>
                    <Cells value="cell.divisions">
                        <ColorMap adaptive-range="false" >
                            <Color value="1"  name="black" />
                            <Color value="25" name="red"   />
                            <Color value="50" name="yellow"/>
                        </ColorMap>
                    </Cells>
                </Plot>
            </Gnuplotter>
    <\Analysis>

Example: Plot multiple panels to screen (CPM cell outlines, PDE with
surface, PDE with isolines), reducing the plot resolution for speed

    <Analysis>
            <Gnuplotter interval="500">
                <Terminal name="wxt"/>
                <Plot>
                    <Cells />
                    <Field symbol-ref="chemoattractant" surface="false" coarsening="2"/>
                </Plot
                <Plot>
                    <Cells />
                    <Field symbol-ref="chemoattractant" isolines="true" coarsening="2"/>
                 </Plot
            </Gnuplotter>
    <\Analysis>

# Haptotaxis {#_group__Haptotaxis}

Haptotaxis

## Description {#_group__LengthConstraint_1Description}

Haptotaxis favors updates in the directions of certain attractants.
Unlike [Chemotaxis](#_group__Chemotaxis) the amount of attractant at the
target site is taken into account, not the gradient of the attractor.

## Example {#_group__ML__Function_1Example}

    <Haptotaxis attractant="10 * agent1" strength="0.1">
    </Haptotaxis>

# InitCellLattice {#_group__InitCellLattice}

InitCellLattice

Initializes lattice of cell for CA-like models.

Initializes lattice of cell for CA-like models.

Initializes a population of cells in which each lattice site is occupied
with exactly 1 cell. Useful to populate CA-like models.

Consequently, each cell has area (2D) or volume (3D) ![](form_10.png) .

Basically a shorthand for the same functionality of InitRectangle.

## Example {#_group__ML__Function_1Example}

Populate a lattice with cells:

    <InitCellLattice />

Equivalent to InitRectangle for a 20x20 lattice:

    <InitRectangle mode="regular" numberOfCells="400">
        <Dimensions size="20,20,0" origin="0.0, 0.0, 0.0"/>
    </InitRectangle>

# InitCellObjects {#_group__InitCellObjects}

InitCellObjects

Initialize a population of cells with predefined geometrical objects in
a regular lattice.

Initialize a population of cells with predefined geometrical objects in
a regular lattice.

Initializes cells with defined shapes in 2D and 3D, arranged in a
regular fashion.

Supported shapes (2D/3D) are: square / box, circle / sphere, ellipse /
ellipsoid, bar / cylinder.

**mode** (default=distance): Specifies how conflicts are resolved in
case multiple objects claim the same lattice node.

-   order: object with lowest celltype.id (as given by order of CellType
    definitions) is assigned

-   distance: closest object is assigned

**Arrangement:** the layout of the cell objects

-   **repetitions:** (x,y,z) vector specifying the number of objects to
    create along x,y,z axes (in units of object number).

-   **displacements:** (x,y,z) vector specifying the distance between
    objects along x,y,z axes (in units of lattice sites).

-   **random_displacement:** (default=0.0): Optional value specifying a
    random displacement of objects from the regular arrangement (in
    units of lattice sites).

**Object:** specify the type and size of geometrical object

-   **Point:**

    -   point: position of first point

-   **Box:** specified by origin and size

    -   origin: position of bottomleft position of first object

    -   size: object size along the 3 box axis

    -   rotation: rotate the box around z, y, and x-axis respectively

-   **Sphere:** specified by center and radius

    -   center: center of initial object

    -   radius: radius of sphere

-   **Ellipsoid:** specified by center and length of semi-principal axes

    -   center: center of initial object

    -   axes: length of semi-principal axes along x, y, z directions

    -   rotation: rotate the ellipsoid around z, y, and x-axis
        respectively

-   **Cylinder:**

    -   origin: origin of cylinder, i.e. one end

    -   length: vector to the other cylinder end

    -   radius: radius of cylinder

-   **Hexagon:**

    -   center: center of initial object

    -   radius: radius of the circumcircle

    -   height: height of the hex prism in 3D

    -   rotation: rotate the ellipsoid around z, y, and x-axis
        respectively

## Examples {#_group__ML__VectorRule_1Examples}

Initializing a single circle or sphere:

    <InitCellObjects mode="distance">
        <Arrangement repetitions="1,1,1" displacements="0,0,0">
            <Sphere center="50,50,0" radius="50"/>
        </Arrangement>
    </InitCellObjects>

Initializing 6\*6 circles or spheres:

    <InitCellObjects mode="distance">
        <Arrangement repetitions="6,6,0" displacements="10,10,0">
            <Sphere center="10,10,0" radius="10"/>
        </Arrangement>
    </InitCellObjects>

Hexagonal tesselation: choose lattice size (repetitions.x \*
displacements.x, repetitions.y \* displacements.y, 0)

    <InitCellObjects mode="distance">
        <Arrangement repetitions="16,14,0" displacements="32,40,0">
            <Sphere radius="30" center="16,16,0"/>
        </Arrangement>
        <Arrangement repetitions="16,14,0" displacements="32,40,0">
            <Sphere radius="30" center="32,40,0"/>
        </Arrangement>
    </InitCellObjects>

Rhombic dodecahedrons using expressions Choose lattice size (r.x\*d.x,
r.y\*d.y, r.z\*d.z)

    <Global>
       <ConstantVector symbol="r" name="repetitions" value="5,4,3" />
       <ConstantVector symbol="p" name="position" value="16,16,16" />
       <ConstantVector symbol="d" name="displacements" value="2*p.x, 3*p.y, 3*p.z" />
    </Global>
    ...
    <InitCellObjects mode="distance">
        <Arrangement repetitions="r" displacements="d">
            <Sphere radius="21" center="p"/>
        </Arrangement>
        <Arrangement repetitions="r" displacements="d">
            <Sphere radius="21" center="2*p.x, 2.5*p.y, p.z"/>
        </Arrangement>
        <Arrangement repetitions="r" displacements="d">
            <Sphere radius="21" center="2*p.x, 1.5*p.y, 2.5*p.z"/>
        </Arrangement>
        <Arrangement repetitions="r" displacements="d">
            <Sphere radius="21" center="p.x, 3*p.y, 2.5*p.z"/>
        </Arrangement>
    </InitCellObjects>

# InitCircle {#_group__InitCircle}

InitCircle

Initializes cells as single nodes arranged in a circle.

Initializes cells as single nodes arranged in a circle.

## Description {#_group__LengthConstraint_1Description}

InitCircle puts a number of cells in an either circular region,
depending on the lattice structure.

The Dimensions tag determines the center and the radius of the circular
region.

Cells are seeded randomly, or in a regular structure. In case of a
regular structure, deviations from this regularity can be induced by
using a uniform random displacement.

## Examples {#_group__ML__VectorRule_1Examples}

100 cells in regular intervals around origin

    <InitCircle number-of-cells="100" mode="regular">
        <Dimensions center="0, 0, 0" radius="10"/>
    </InitCircle>

Almost regular placement of cells in a circular region in center of
lattice

    <InitCircle number-of-cells="rand_norm(100,10)" mode="regular" random_displacement="0.05*size.x" >
        <Dimensions center="size.x/2, size.y/2, 0" radius="size.x/2"/>
    </InitCircle>

Random placement of cells in a circular region at the origin of the
lattice

    <InitCircle number-of-cells="0.01 * (size.x * size.y)" mode="random" >
        <Dimensions center="0, 0, 0" radius="size.x/3"/>
    </InitCircle>

# InitDistribute {#_group__InitDistribute}

InitDistribute

Places and initializes cells randomly in space the lattice with certain
probability.

Places and initializes cells randomly in space the lattice with certain
probability.

## Description {#_group__LengthConstraint_1Description}

Places **number-of-cells** cells randomly in space using **probability**
as likelyhood bias.

## Example {#_group__ML__Function_1Example}

    <InitDistribute number-of-cells="100" probability="1+sin(0.05*size.x)" />

# InitHexLattice {#_group__InitHexLattice}

InitHexLattice

Initializes lattice of cell for CA-like models.

Initializes lattice of cell for CA-like models.

Initializes a population of cells in which each lattice site is occupied
with exactly 1 cell. Useful to populate CA-like models.

Consequently, each cell has area (2D) or volume (3D) ![](form_10.png) .

Basically a shorthand for the same functionality of InitRectangle.

## Example {#_group__ML__Function_1Example}

Populate a lattice with cells:

    <InitHexLattice />

Equivalent to InitRectangle for a 20x20 lattice:

    <InitRectangle mode="regular" numberOfCells="400">
        <Dimensions size="20,20,0" origin="0.0, 0.0, 0.0"/>
    </InitRectangle>

# Population Initializer Plugins {#_group__InitializerPlugins}

Population Initializer Plugins

## Modules {.unnumbered}

-   [CSVReader](#_group__CSVReader)

    Initializes cell population from CSV file.

-   [InitCellLattice](#_group__InitCellLattice)

    Initializes lattice of cell for CA-like models.

-   [InitCellObjects](#_group__InitCellObjects)

    Initialize a population of cells with predefined geometrical objects
    in a regular lattice.

-   [InitCircle](#_group__InitCircle)

    Initializes cells as single nodes arranged in a circle.

-   [InitDistribute](#_group__InitDistribute)

    Places and initializes cells randomly in space the lattice with
    certain probability.

-   [InitHexLattice](#_group__InitHexLattice)

    Initializes lattice of cell for CA-like models.

-   [InitPoissonDisc](#_group__InitPoissonDisc)

    Arranges cells approximately equidistantly according to Poisson Disk
    Sampling.

-   [InitRectangle](#_group__InitRectangle)

    Initializes cells as single nodes arranged in a rectangle.

-   [InitVoronoi](#_group__InitVoronoi)

    Compute cell areas according to the Voronoi tesselation.

-   [TIFFReader](#_group__TIFFReader)

## Detailed Description

# InitPoissonDisc {#_group__InitPoissonDisc}

InitPoissonDisc

Arranges cells approximately equidistantly according to Poisson Disk
Sampling.

Arranges cells approximately equidistantly according to Poisson Disk
Sampling.

## Description {#_group__LengthConstraint_1Description}

Arranges approximately equidistance cells according to Poisson Disk
Sampling using Robert Bridson's algorithm. Attempts to arrange
**number-of-cells** but will generate less cells.

Only applicable to 2D lattices with square structure.

Implementation from:
<https://github.com/corporateshark/poisson-disk-generator>

## Example {#_group__ML__Function_1Example}

Try to initialize 500 cells in the given lattice:

    <InitPoissonDisc number-of-cells="500"/>

# InitRectangle {#_group__InitRectangle}

InitRectangle

Initializes cells as single nodes arranged in a rectangle.

Initializes cells as single nodes arranged in a rectangle.

## Description {#_group__LengthConstraint_1Description}

Arranges a number of cells in an either a rectangular (or cubic) region.

If **mode** is \'regular\'. Cells are seeded randomly, or in a regular
structure. In case of a regular structure, deviations from this
regularity can be induced by using a uniform random offset.

The **Dimensions** tag determines the origin of the left lower corner
and the size of the region.

## Example {#_group__ML__Function_1Example}

    <InitRectangle number-of-cells="100" mode="regular">
        <Dimensions origin="0 0 0" size="100 100 1"/>
    </InitRectangle>

    <InitRectangle number-of-cells="rand_norm(100,10)" mode="regular" random-offset="0.05*size.x" >
        <Dimensions origin="0, 0, 0" size="size.x/2, size.y, size.z"/>
    </InitRectangle>

    <InitRectangle number-of-cells="0.01 * (size.x * size.y)" mode="random" >
        <Dimensions origin="size.x/4, size.y/4, size.z/2" size="size.x/2, size.y/2, size.z/2"/>
    </InitRectangle>

# InitVoronoi {#_group__InitVoronoi}

InitVoronoi

Compute cell areas according to the Voronoi tesselation.

Compute cell areas according to the Voronoi tesselation.

Computes the Voronoi tesselation of the empty areas and sets cell IDs
according to this tesselation. Note that cell positions have to be
specified beforehand (with some other plugin is specified earlier).

-   Assumes cell positions have already been initialized.

-   Only uses non-occupied lattice nodes.

-   Respects [Domain](#_group__ML__Domain)

## Example {#_group__ML__Function_1Example}

    <InitVoronoi />

# InsertMedium {#_group__InsertMedium}

InsertMedium

Inserts medium nodes randomly along a cell membrane.

Inserts medium nodes randomly along a cell membrane.

Inserts medium nodes randomly along a cell membrane.

In CPM models of continuous cell monolayers, without medium, tissues
cannot be disrupted, even when under tension. Randomly inserting medium
nodes can be used to compensate for this behavior.

Each Monte Carlo step:

-   select a random cell

-   if it already have medium nodes around it, return

-   else, select a random node around the cell

-   convert this node into medium

-   **Condition** (default = true): expression to evaluate to trigger
    inserting medium

## Reference {#_group__LengthConstraint_1Reference}

-   Jos Kafer, Takashi Hayashi, Athanasius F.M. Maree, Richard W.
    Carthew and Francois Graner, Cell adhesion and cortex contractility
    determine cell patterning in the Drosophila retina, PNAS, 2007.

## Example {#_group__ML__Function_1Example}

    <InsertMedium/>

# Instantaneous Process Plugins {#_group__InstantaneousProcessPlugins}

Instantaneous Process Plugins

## Modules {.unnumbered}

-   [AddCell](#_group__ML__AddCell)

    Add new cells based during simulation.

-   [CellDeath](#_group__CellDeath)

    Remove cell based on a condition.

-   [CellDivision](#_group__ML__CellDivision)

    Divide cell based on condition.

-   [ChangeCellType](#_group__ChangeCellType)

    Conditionally alters CellType of cell.

-   [Event](#_group__ML__Event)

-   [InsertMedium](#_group__InsertMedium)

    Inserts medium nodes randomly along a cell membrane.

## Detailed Description

The following plugins represent instantaneous processes, i.e. these
processes do not take time to finish.

# Interaction Plugins {#_group__InteractionPlugins}

Interaction Plugins

Plugins that determine cell interactions in terms of energies.

## Modules {.unnumbered}

-   [AddOnAdhesion](#_group__ML__AddOnAdhesion)

    Additive interaction energy based on a global expression
    (deprecated)

-   [HeterophilicAdhesion](#_group__ML__HeterophilicAdhesion)

    Heterophilic adhesive interaction between neighboring CPM cells.

-   [HomophilicAdhesion](#_group__ML__HomophilicAdhesion)

    Homophilic adhesive interaction between neighboring CPM cells.

## Detailed Description

Plugins that determine cell interactions in terms of energies.

# InterfaceConstraint {#_group__InterfaceConstraint}

InterfaceConstraint

Penalizes deviations from target cell interface length (2D) or interface
area (3D) with cells of another cell type.

Penalizes deviations from target cell interface length (2D) or interface
area (3D) with cells of another cell type.

The interface constraint penalizes deviations of the cell interface
length (2D) or interface area ![](form_73.png) with cells of another
cell type ![](form_74.png) from a given target ![](form_75.png) .

This models a cell interface length conservation mechanism.

The Hamiltonian for cell ![](form_76.png) is given by ![](form_77.png)

where

-   ![](form_31.png) is the id of a cell.

-   ![](form_78.png) interface length of cells ![](form_79.png) and
    ![](form_80.png) .

-   ![](form_75.png) is the target interface size of cell
    ![](form_81.png) with cells of type ![](form_82.png) .

-   ![](form_83.png) is strength of the constraint.

## Input {#_group__LengthConstraint_1Input}

### Required {#_group__InterfaceConstraint_1autotoc_md15}

-   *type*: Sum of the interface lengths with cells of this cell type
    will be constrained.

-   *target*: Target interace length (2D) or interface area (3D) of a
    cell.

-   *strength*: Strength of the interface constraint.

# LengthConstraint {#_group__LengthConstraint}

LengthConstraint

Penalizes deviations from target cell length.

Penalizes deviations from target cell length.

## Description {#_group__LengthConstraint_1Description}

### Mode {#_group__LengthConstraint_1Length}

The length constraint penalizes deviations of the length of a cell
![](form_84.png) from a given target length ![](form_85.png) , specified
in units of lattice sites.

The length of a cell is estimated as the length of the semimajor axis of
an ellipsoid approximation of the cell shape, using the inertia tensor.

The Hamiltonian is given by: ![](form_86.png)

![](form_87.png) where

-   ![](form_88.png) is the strength of the constraint

-   ![](form_89.png) is the current length of cell ![](form_31.png) at
    time ![](form_59.png)

-   ![](form_90.png) is the projected length of cell ![](form_31.png) at
    time ![](form_59.png) (if updated would be accepted)

-   ![](form_85.png) is the target length of cell ![](form_31.png) at
    time ![](form_59.png)

### Mode {#_group__LengthConstraint_1Eccentricity}

The length constraint penalizes deviations of the eccentricity of a cell
![](form_91.png) from a given target ![](form_92.png) .

The eccentricity is derived from the ellipsoid approximation of the cell
shape, using the inertia tensor.

The Hamiltonian is given by: ![](form_93.png)

## Input {#_group__LengthConstraint_1Input}

-   *mode*: Selects to constrain either eength or eccentricity.

-   *target*: Expression describing the target cell length. This may be
    a constant (e.g. \"1.0\"), a symbol (e.g. \"St\"), or an expression
    (e.g. \"S0 \* 2.0\")

-   *strength*: Expression describing the strength of the length
    constraint. This may be a constant (e.g. \"2.0\"), a symbol (e.g.
    \"Ss\"), or an expression (e.g. \"S0 \* 2.0\")

## Notes {#_group__LengthConstraint_1Notes}

-   This constraint is not safe against periodic boundary conditions.

-   Use together with \"ConnectivityConstraint\" plugin to prevent cell
    breakup.

-   This plugin is optimized to determine the cell length using
    incremental updates, preventing the need to recompute the entire
    inertia tensor on every call.

-   Acknowledgement: Incremental updating is implemented by Robert
    Muller (ZIH, TU Dresden)

## Reference {#_group__LengthConstraint_1Reference}

Zajac M, Jones GL, Glazier JA. Simulating convergent extension by way of
anisotropic differential adhesion. J Theor Biol. 222:247--259, 2003.

## Example {#_group__ML__Function_1Example}

# Logger {#_group__Logger}

Logger

Writes output to text file. Optionally, plots graphs.

Writes output to text file. Optionally, plots graphs.

## Description {#_group__LengthConstraint_1Description}

Versatile interface to

1.  write simulation data to files in CSV and matrix format and

2.  draw a variety of plots such as time plots, phase plots, space-time
    plots, surface plots, etc.

### Input {#_group__LengthConstraint_1Input}

-   **time-step** (optional): time between logging events. If
    unspecified adopts to the frequency of input updates. Setting
    **time-step\<=0** will log only the final state of the simulation.

-   **name** (optional, default=none): displayed in GUI, only for
    user-convenience

-   **force-node-granularity** (optional, default=false): force logging
    per node in a grid-like fashion.

-   **exclude-medium** (optional, default=true): when logging cell
    properties, only include biological cells.

#### Symbol (required) {#_group__Logger_1Symbol}

Specifies at one or more symbols to write to data file. Symbol can be
flexibly combined, but the data format is determined by the symbol with
the smallest granularity.

-   **symbol-ref** (required): symbol referring to e.g. a global
    [Variable](#_group__ML__Variable), a cell
    [Property](#_group__ML__Property), a
    [MembraneProperty](#_group__ML__MembraneProperty), or a
    [Field](#_group__ML__Field).

### Output (required) {#_group__Logger_1Output}

Specifies the details of the output file

-   **file-format** (optional, default=automatic): output can be written
    in CSV or matrix format (for surface plots)

-   **header** (optional, default=true): whether or not to write symbol
    names as header

-   **separator** (optional, default=\"tab\"): specifies delimiter
    between values

-   **file-name** (optional, default=automatic): filename are created
    automatically by default, but are overridden if specified

-   **file-numbering** (optional, default=time): filenames are named
    according to simulation time or incremental numbering

-   **file-separation** (optional, default=none): writes separate files
    for time, cells or both (cell+time)

### Restriction (optional) {#_group__Logger_1Restriction}

Restrict the data query to a certain slice, a cell type or certain cell
IDs.

-   **Slice:** restrict query to slice (note: requires node granularity)

    -   **axis** (required): x,y,z axis to slice

    -   **value** (required): position along axis at which to slice the
        space (can be expression)

-   **Celltype:** restrict query to cell of specific celltype

    -   **celltype** (required): name of
        [CellType](#_group__ML__CellType) to query

-   **Cells:** write values of [Property](#_group__ML__Property) or
    [MembraneProperty](#_group__ML__MembraneProperty)

    -   **cell-ids** (required): range of cell IDs to include. Syntax:

        -   list of comma-separated IDs: \"1,2,5\", or

        -   range of IDs with dash: \"4-8\", or

        -   combination of list and range: \"12-15, 24-28\".

-   **condition** (optional, default=1): condition used in addition to
    constraint the query to certain cells/nodes fulfilling the condition

-   **domain-only** (optional, default=true): if the lattice is confined
    to a domain, only query nodes within domain. If false, also include
    nodes outside of domain

-   **force-node-granularity** (optional, default=false): granularity of
    nodes is automatically detected by default, but may be overridden if
    specified

### Plots (optional) {#_group__Logger_1Plots}

Specifies one or more plots, generated from the data in the written data
file.

#### Plot {#_group__Logger_1Plot}

Symbols can be selected for X and Y dimensions + color and the range of
time points can be selected.

-   **X-axis** (required): specify a symbol to use as x axis

    -   **logarithmic** (optional, default=false): use logarithmic scale

    -   **minimum** (optional, default=none): fix minimum of axis

    -   **maximum** (optional, default=none): fix maximum of axis

    -   **palette** (optional): choose a color scale

    -   **reverse-palette** (optional, default=\"false\"): reverse the
        color scale

-   **Y-axis** (required): specify one or more symbols to show on y-axis

    -   options as for X-axis

-   **Color-bar** (optional): specify a symbol to color points or lines

    -   options as for X-axis

-   **Range** (optional): select time range or filter data to include in
    plot:

    -   **Data** (optional): skip data points using gnuplot\'s \'every\'
        keyword

        -   **first-line** (optional)

        -   **last-line** (optional)

        -   **increment** (optional) This yields: every
            \[increment\]::\[first-line\]::\[last-line\]

    -   **Time** (optional): select time range of data to include

        -   all: plot all time points

        -   since last plot: only plot time points since last plot event

        -   history: only plot time points between current and
            (current - history). Requires \"history\" value to be
            specified.

        -   current: only plot time point

        -   **history** (optional): length of history to plot, in units
            of simulation time (only used when mode=\"history\")

-   **Terminal** (required): select an output format

    -   **terminal** (required, default=png): select on-screen or file
        terminal (e.g. wxt, aqua, png, jpg, svg, pdf)

    -   **plot-size** (optional): size of the plot, e.g. 600,400,0

    -   **file-numbering** (optional, default=time): filenames are named
        according to simulation time or incremental numbering

-   **Style** (optonal): configure the style of the plot

    -   **decorate** (optional, default=false): hide axis labels, legend
        and colorbar

    -   **style** (optional, default=points): points, lines, or
        linespoints

    -   **line-width** (optional, default=1): line width if using lines
        or linespoints

    -   **point-size** (optional, default=1): point size if using points
        or linespoints

    -   **grid** (optional, default=false): draw dotted line in plot at
        major ticks

-   **log-commands** (optional, default=false): write gnuplot commands
    to file

-   **time-step** (optional): interval to create plot.

    -   If omitted, plots every 10th logging step (Logger/@time-step \*
        10)

    -   Special values:

        -   negative : never

        -   0 : end of simulation

-   **title** (optional, default=none): Title caption for the Plot

#### SurfacePlot (optional) {#_group__Logger_1SurfacePlot}

Draws a surface plot (e.g. heatmap) from data in matrix format

-   **Color-bar** (optional): specify a symbol to color points or lines

    -   **logarithmic** (optional, default=false): use logarithmic scale

    -   **minimum** (optional, default=none): fix minimum of axis

    -   **maximum** (optional, default=none): fix maximum of axis

    -   **palette** (optional): choose a color scale

    -   **reverse-palette** (optional, default=\"false\"): reverse the
        color scale

-   **Terminal** (required): select an output format

    -   **terminal** (required, default=png): select on-screen or file
        terminal (e.g. wxt, aqua, png, jpg, svg, pdf)

    -   **plot-size** (optional): size of the plot, e.g. 600,400,0

    -   **file-numbering** (optional, default=time): filenames are named
        according to simulation time or incremental numbering

-   **log-commands** (optional, default=false): write gnuplot commands
    to file

-   **time-step** (optional, default=0): interval to create plot.

    -   If omitted, plots every 10th logging step (Logger/@time-step \*
        10)

    -   Special values:

        -   negative : never

        -   0 : end of simulation

-   **name** (optional, default=none): displayed in GUI, only for
    user-convenience

## Examples {#_group__ML__VectorRule_1Examples}

The example below assume the following symbols to be defined:

    TimeSymbol symbol="time"
    SpaceSymbol symbol="space"
    Field symbol="f"
    Property symbol="p"
    MembraneProperty symbol="m"

### Two variables: time and phase plots {#_group__Logger_1Two}

Log two global Variables (N and P) n the format below (see PredatorPrey
example). And create a timeplot with multiple variables plotting on
Y-axis. And draw a phase plot with N and P on both axis, indicating time
as colors.

    <Logger time-step="5">
        <Column>
            <Global symbol-ref="N"/>
        </Column>
        <Column>
            <Global symbol-ref="P"/>
        </Column>
        <Output/>
        <Plot lines-or-points="lines" name="time plot">
            <X-axis>
                <Column symbol-ref="time"/>
            </X-axis>
            <Y-axis>
                <Column symbol-ref="N"/>
                <Column symbol-ref="P"/>
            </Y-axis>
        </Plot>
        <Plot lines-or-points="lines" name="phase plot">
            <X-axis>
                <Column symbol-ref="N"/>
            </X-axis>
            <Y-axis>
                <Column symbol-ref="P"/>
            </Y-axis>
            <Color-bar>
                <Column symbol-ref="time"/>
            </Color-bar>
        </Plot>
    </Logger>

Output format:

    time    N   P
    0   0.1 0.5
    5   0.102334    0.495966
    10  0.105018    0.492469
    ...

### Cell properties: colored time and phase plots {#_group__Logger_1Cell}

Log cell properties in a population of cells (see LateralSignaling
example). And create a time plot with points colored according to a cell
property. And draw a phase plot with points colored according to time.

    <Logger time-step="0.05">
        <Column>
            <Cells symbol-ref="X"/>
        </Column>
        <Output/>
        <Plot point-size="0.5" name="time plot">
            <X-axis>
                <Column symbol-ref="time"/>
            </X-axis>
            <Y-axis>
                <Column symbol-ref="X"/>
            </Y-axis>
            <Color-bar>
                <Column symbol-ref="Y"/>
            </Color-bar>
        </Plot>
        <Column>
            <Cells symbol-ref="Y"/>
        </Column>
        <Plot point-size="0.5" name="phase plot">
            <X-axis>
                <Column symbol-ref="X"/>
            </X-axis>
            <Y-axis>
                <Column symbol-ref="Y"/>
            </Y-axis>
            <Color-bar>
                <Column symbol-ref="t"/>
            </Color-bar>
        </Plot>
    </Logger>

Output format:

    time    cell.id X   Y
    0   1   0   0
    0   2   0   0
    ...
    0.05    1   0.0580316   0.0576386
    0.05    2   0.0580715   0.0576858
    ...

###  {#_}

Log a slice of two Fields (\'a\' and \'i\') in the following format:
Create a space-time plot with time on X-axis, space on Y-axis and colors
indicating concentration of \'a\'. Draw a concentration profile of \'a\'
at the slice at the current time point.

    <Logger time-step="50">
        <Column>
            <Field symbol-ref="a"/>
        </Column>
        <Column>
            <Field symbol-ref="i"/>
        </Column>
        <Slice value="size.y/2" axis="y"/>
        <Output/>
        <Plot time-step="2500" name="space-time plot">
            <X-axis>
                <Column symbol-ref="time"/>
            </X-axis>
            <Y-axis>
                <Column symbol-ref="space.x"/>
            </Y-axis>
            <Color-bar>
                <Column symbol-ref="a"/>
            </Color-bar>
        </Plot>
        <Plot time-range="current" lines-or-points="linespoints" time-step="2500" name="profile plot">
            <X-axis>
                <Column symbol-ref="space.x"/>
            </X-axis>
            <Y-axis>
                <Column symbol-ref="a"/>
            </Y-axis>
        </Plot>
    </Logger>

Output format:

    time    space.x space.y space.z a   i
    0   0   50  0   0.347683    0.1
    0   1   50  0   0.277144    0.1
    0   2   50  0   0.622711    0.1
    ...
    25  0   50  0   0.349179    0.0504817
    25  1   50  0   0.347195    0.0504857
    25  2   50  0   0.390495    0.0504852
    ...

# MathExpressions {#_group__MathExpressions}

MathExpressions

## Modules {.unnumbered}

-   [DiffEqn](#_group__ML__DiffEqn)

-   [Equation](#_group__ML__Equation)

-   [Event](#_group__ML__Event)

-   [Function](#_group__ML__Function)

    Parametric Function declaration.

-   [System](#_group__ML__System)

-   [VectorEquation](#_group__ML__VectorEquation)

-   [VectorFunction](#_group__ML__VectorFunction)

## Detailed Description

Mathematical expressions to be evaluated during run-time. The vector
version uses by default the component-wise \'x,y,z\' notation, or
alternative spherical notations as offered by **notation** attribute.

### Operators: {#_group__MathExpressions_1Available}

+, -, \*, /, \^, =, \>=, \<=, !=, ==, \<, \> and, or, xor, !

Ternary operator: //condition ? \[true value\] : \[false value\]//

-   Depending on value of the condition, only the respective result
    expression is evaluated. This is may be more performant than the \\i
    if function.

### Functions {#_group__MathExpressions_1Functions}

-   Logical: if(\[condition\], \[then\], \[else\]), and, or, xor

-   Trigonometric: sin, cos, tan, asin, acos, atan, sinh, cosh, tanh,
    asinh, acosh, atanh

-   Exponential: log2, log10, ln, exp, pow, sqrt,

-   others: sign, rint, abs, min, max, sum, avg, mod

MathML compatibility Functions\*\*:

-   piecewise(\[value\],\[condition\], (\[value\],\[condition\],)\*
    ,\[else value\])

-   ceil, floor, rem, quotient, factorial, root

-   arcsin, arccos, arctan, arcsinh, arccosh, arctanh

-   lt, leq, eq, neq, geq, gt

Additional functions can be defined using
[Function](#_group__ML__Function).

### Random number generators {#_group__MathExpressions_1Random}

-   rand_uni(\[min\], \[max\])

-   rand_norm(\[mean\], \[stdev\])

-   rand_gamma(\[shape\], \[scale\])

-   rand_invgamma(\[shape\], \[scale\])

-   rand_int(\[min\], \[max\])

-   rand_bool()

# Miscellaneous Plugins {#_group__MiscellaneousPlugins}

Miscellaneous Plugins

Plugins for population management and auxiliary plugins.

## Modules {.unnumbered}

-   [AddCell](#_group__ML__AddCell)

    Add new cells based during simulation.

-   [CellDeath](#_group__CellDeath)

    Remove cell based on a condition.

-   [CellDivision](#_group__ML__CellDivision)

    Divide cell based on condition.

-   [ChangeCellType](#_group__ChangeCellType)

    Conditionally alters CellType of cell.

-   [InsertMedium](#_group__InsertMedium)

    Inserts medium nodes randomly along a cell membrane.

## Detailed Description

Plugins for population management and auxiliary plugins.

# AddCell {#_group__ML__AddCell}

AddCell

Add new cells based during simulation.

Add new cells based during simulation.

Create new cells during simulation at positions given by a spatial
probability distribution. AddCell runs every MCS and places cells given
by **Count**. Fractional counts are realized statistically.

-   **Count:** Expression describing how many cells to be created.
    Fractional counts are realized statistically.

-   **Distribution:** Expression describing the spatial probability
    distribution (normalized to 1 internally).

-   **overwrite** (default=false): Whether or not a new cell should be
    created at a location occupied by another cell.

-   **Logging** (optional): Log all triggered cell adding events to
    file, including all symbols defined under this tag.

-   **Triggers** (optional): [System](#_classSystem) of Rules to be
    triggered after a cell was added.

## Example {#_group__ML__Function_1Example}

Adding a new cell every MCS with increasing probability along x axis,
automatically scheduled

    <AddCell>
        <Count> 1 </Count>
        <Distribution> l.x / size.x </Distribution>
    </AddCell>

Adding cells with normal distribution centered in middle of lattice
(stdev=25). The fractional count 0.01 is realized statistically, such
that on average the every 100 MCS a cell is created.

    <AddCell>
        <Count> 0.01 </Count>
        <Distribution> exp(-((l.x-size.x/2)^2 + (l.y-size.y/2)^2) / (2*25^2) )</Distribution>
    </AddCell>

Adding cells with uniform spatial distribution, setting properties of
new cell with Triggers

    <AddCell>
        <Count> p > 1 </Count>
        <Distribution> 1 </Distribution>
        <Triggers>
            <Rule symbol-ref="birth_time"> time </Rule>
        </Triggers>
    </AddCell>

# AddOnAdhesion {#_group__ML__AddOnAdhesion}

AddOnAdhesion

Additive interaction energy based on a global expression (deprecated)

Additive interaction energy based on a global expression (deprecated)

**Deprecation note: This plugin is deprecated and might be removed
without further notice. It\'s functionality superseded by expression
usage in Contact/value. It\'s only conserved for compatibility
reasons.**

Increases adhesion (i.e. decreases cell-contact energy) between
neighboring CPM cells. Expression may use globally defined symbols that
map to cell or membrane property.

Changes cell-contact energy depending on the amount of adhesive
![](form_13.png) present in the cells (additive).

![](form_14.png) with units energy per node length.

-   **adhesive:** Expression describing amount of adhesive molecules.
    This may be a symbol representing a cell or membrane property (e.g.
    \"c\") or an expression (e.g. \"10 \* c\").

-   **strength:** (default=1): Expression describing strength of
    adhesion. This may be a symbol representing a cell or membrane
    property (e.g. \"s\") or an expression (e.g. \"10 \* s\").

## Examples {#_group__ML__VectorRule_1Examples}

Using cell or membrane property \'c\' as adhesive (strength = 1.0 by
default)

    <AddonAdhesion adhesive="c" />

Both adhesive and strength can be provided as expression.

        <AddonAdhesion adhesive="10.0 * c" strength="t / 10.0" />

# Analysis {#_group__ML__Analysis}

Analysis

## Modules {.unnumbered}

-   [CellTracker](#_group__CellTracker)

    Writes cell tracks in XML format.

-   [ClusteringTracker](#_group__ML__ClusteringTracker)

    Identifies and writes distribution of cell clusters within a single
    celltype.

-   [Constant](#_group__ML__Constant)

-   [ConstantVector](#_group__ML__ConstantVector)

-   [ContactLogger](#_group__ContactLogger)

    Write the contacts and contact lengths between cells to file.

-   [DisplacementTracker](#_group__ML__DisplacementTracker)

    Track the cell displacement of a population.

-   [External](#_group__ML__External)

    Execute external shell script.

-   [Function](#_group__ML__Function)

    Parametric Function declaration.

-   [Gnuplotter](#_group__Gnuplotter)

    Visualisation of spatial simulation states (cells, fields) using
    GnuPlot.

-   [HistogramLogger](#_group__ML__HistogramLogger)

    Computation of frequency distributions and visualisation of
    histograms.

-   [Logger](#_group__Logger)

    Writes output to text file. Optionally, plots graphs.

-   [TiffPlotter](#_group__TiffPlotter)

    Writes cells and fields to multipage TIFF images.

-   [VectorFunction](#_group__ML__VectorFunction)

-   [VtkPlotter](#_group__VtkPlotter)

    Writes cells and fields to legacy VTK files.

## Detailed Description

Analyis section allows definition of [Analysis
Plugins](#_group__AnalysisPlugins) for data analysis, logging and
visualization. Most analysers produce output in terms of text files,
xml-files and/or images.

# CellDivision {#_group__ML__CellDivision}

CellDivision

Divide cell based on condition.

Divide cell based on condition.

Triggers cell division when condition is satisfied.

First, a division plane is calculated, through the cell\'s center of
mass (see orientation options below). Then, the nodes of the mother cell
on either side of this plane are allocated to two new daughter cells.

By default, all property values are copied from the mother to the two
daughter cells. This can be overridden using **Triggers** to set or
initialize the properties of daughter cells. See example below.

To specify daughter-specific properties (to model e.g. asymmetric cell
division), you can use the daughterID option. This defines a symbolic
handle (value 1 or 2) for the two daughters that can be used in the
Triggers. See example below.

-   **condition:** Expression defining the condition under which a cell
    should divide

-   **division-plane**: Plane of division, through cell\'s center of
    mass.

    -   major: longest axis in ellipsoid approximation of cell shape
        gives the normal vector of the division plane

    -   minor: shortest axis in ellipsoid approximation of cell shape
        gives the normal vector of the division plane

    -   random: randomly oriented division plane

    -   oriented: user-specified division plane (must be given as normal
        vector in \'orientation\')

-   **write_log** (default none): Create log file about cell divisions
    in one of the following formats: CSV (Time, mother ID, daughter
    IDs), NEWICK (<https://en.wikipedia.org/wiki/Newick_format>), or DOT
    (<https://en.wikipedia.org/wiki/DOT_(graph_description_language)>)
    format.

-   **daughterID** (optional): Local symbol that provides unique IDs (1
    or 2) for the two daughter cells to be used in Triggers, e.g. to
    model asymmetric cell division.

-   **orientation** (optional): Vector (or vectorexpression) giving the
    normal vector of the division plane. Only used (and required) if
    division-plane=\"oriented\".

-   **trigger:** (optional): Cell division is triggered whenever the
    condition turns to true (**on-change**, default) or whenever the
    condition is found true (**when-true**, checked every MCS).

-   **Triggers** (optional): a [System](#_classSystem) of Rules that are
    triggered for both daughter cells after cell division.

-   **Logging** (optional): Log all triggered cell division events to
    file, including all symbols defined under this tag.

## Examples {#_group__ML__VectorRule_1Examples}

Divide with random orientation when cell volume doubles.

    <CellDivision   condition="V >= (2.0 * V0)" 
                    division_plane="random" />

Divide every 1000 time steps along a user-specified orientation.

    <CellDivision   condition="mod(time, 1000) == 0" 
                    division_plane="oriented" 
                    orientation="vector.x, vector.y, vector.z" />

Using Triggers to specify properties after cell division (asymmetric
division). Symbol \'Vt\' is here set to a daughter-specific value with
\'daughterID\',

    <CellDivision condition="V >= (2.0 * V0)" division_plane="major" daughterID="daughter">
        <Triggers>
            <Rule symbol-ref="Vt">
                <Expression>
                    if( daughter == 1, 100, 50 )
                </Expression>
            </Rule>
            <Rule symbol-ref="divisions">
                <Expression>
                    divisions + 1
                </Expression>
            </Rule>
        </Triggers>
    </CellDivision>

# CellPopulations {#_group__ML__CellPopulations}

CellPopulations

## Modules {.unnumbered}

-   [Population](#_group__ML__Population)

## Detailed Description

Definition of a spatial cell configuration of the CPM.

[Population](#_group__ML__Population) elements specify the initial
conditions or spatial cell configuration.

**BoundaryValue** defines the value of the [CPM](#_group__ML__CPM) at
the respective boundary. By default boundary types of the
[Lattice](#_group__ML__Lattice) are set, while `flux` boundaries are
degrades to `constant` boundaries, allowing an influx of the boundary
state into the simulation space. **Note!** Boundaries predefined as
periodic are immutable.

-   **value** the medium class [CellType](#_group__ML__CellType) that
    resides at respective lattice boundary.

-   **type** (optional): override the type of boundary.

    -   `value` (default): just set the boundary value and leave the
        boundary type untouched.

    -   `noflux:` prevent the boundary state to be extended into the
        simulation space.

    -   `constant:` allow an influx of the boundary state into the
        simulation space. **InitialValue** determines the default medium
        class [CellType](#_group__ML__CellType) intially occupying all
        space.

# CellTypes {#_group__ML__CellTypes}

CellTypes

## Modules {.unnumbered}

-   [CellType](#_group__ML__CellType)

## Detailed Description

[Container](#_classContainer) for specification of different
[CellType](#_group__ML__CellType) elements that specify cell properties
and behaviors via plugins.

# CellType {#_group__ML__CellType}

CellType

## Modules {.unnumbered}

-   [AddCell](#_group__ML__AddCell)

    Add new cells based during simulation.

-   [CellDeath](#_group__CellDeath)

    Remove cell based on a condition.

-   [CellDivision](#_group__ML__CellDivision)

    Divide cell based on condition.

-   [ChangeCellType](#_group__ChangeCellType)

    Conditionally alters CellType of cell.

-   [Chemotaxis](#_group__Chemotaxis)

    Energetically favors updates in direction of increasing
    concentration in [Field](#_group__ML__Field).

-   [ConnectivityConstraint](#_group__ConnectivityConstraint)

    Ensures cells remain connected components.

-   [Constant](#_group__ML__Constant)

-   [ConstantVector](#_group__ML__ConstantVector)

-   [DelayProperty](#_group__ML__DelayProperty)

-   [DirectedMotion](#_group__DirectedMotion)

-   [Equation](#_group__ML__Equation)

-   [Event](#_group__ML__Event)

-   [FreezeMotion](#_group__FreezeMotion)

-   [Function](#_group__ML__Function)

    Parametric Function declaration.

-   [Haptotaxis](#_group__Haptotaxis)

-   [InsertMedium](#_group__InsertMedium)

    Inserts medium nodes randomly along a cell membrane.

-   [InterfaceConstraint](#_group__InterfaceConstraint)

    Penalizes deviations from target cell interface length (2D) or
    interface area (3D) with cells of another cell type.

-   [LengthConstraint](#_group__LengthConstraint)

    Penalizes deviations from target cell length.

-   [Mapper](#_group__ML__Mapper)

    Map data from a spatial context into another symbol, usually
    reducing spatial resolution by a mapping function.

-   [MechanicalLink](#_group__ML__MechanicalLink)

-   [MembraneProperty](#_group__ML__MembraneProperty)

-   [MotilityReporter](#_group__MotilityReporter)

    Reports statistics about cell motility.

-   [NeighborhoodReporter](#_group__NeighborhoodReporter)

    Reports data about a node\'s or a cell\'s neighborhood or
    \'microenvironment\'.

-   [NeighborhoodVectorReporter](#_group__NeighborhoodVectorReporter)

    Reports data about a node\'s or a cell\'s neighborhood or
    \'microenvironment\' using Vector input.

-   [PersistentMotion](#_group__PersistentMotion)

-   [Property](#_group__ML__Property)

-   [PropertyVector](#_group__ML__PropertyVector)

-   [Protrusion](#_group__Protrusion)

    Energetically favors updates in region of high protusive activity
    (actin-inspired)

-   [SurfaceConstraint](#_group__SurfaceConstraint)

    Penalizes deviations from target cell perimeter (2D) or surface area
    (3D)

-   [SurfaceMotion](#_group__SurfaceMotion)

-   [System](#_group__ML__System)

-   [Variable](#_group__ML__Variable)

-   [VariableVector](#_group__ML__VariableVector)

-   [VectorEquation](#_group__ML__VectorEquation)

-   [VectorFunction](#_group__ML__VectorFunction)

-   [VectorMapper](#_group__ML__VectorMapper)

    Map vector data from a spatial context into another symbol, usually
    reducing spatial resolution by a mapping function.

-   [VolumeConstraint](#_group__ML__VolumeConstraint)

    Penalizes deviations from target cell area (2D) or volume (3D)

## Detailed Description

A CellType specifies the cell properties, intracellular dynamics and
cell behaviors of the cells within the population. Instead of defining a
specific single cell, CellType defines a blueprint from which specific
single cells can be derived upon initialization and during the
simulation.

CellType can contain any of the following plugin types:

-   [Symbols](#_group__Symbols)

-   [MathExpressions](#_group__MathExpressions)

-   [Cell Motility Plugin](#_group__CellMotilityPlugins)

-   [Cell Shape Plugins](#_group__CellShapePlugins)

-   [Reporter Plugins](#_group__ReporterPlugins)

-   [Miscellaneous Plugins](#_group__MiscellaneousPlugins)

A CellType defines its own [Scope](#_group__Scope). This implies that
symbols defined within a CellType are not normally accessible outside of
the CellType except through **NeighborhoodReporters**. However, if the
identical symbol is defined in all CellTypes, then it also becomes
accessible at the global scope.

In addition, celltype scopes intrinsically provide preset symbols to
access cell properties

-   cell.id

-   cell.type

-   cell.volume Non-medium types also provide

-   cell.center

-   cell.orientation

-   cell.surface

The initial configuration of the cell population must be specified in
the [CellPopulations](#_group__ML__CellPopulations) section.

# Cell {#_group__ML__Cell}

Cell

Stores cell state.

Stores cell state.

This element is used to store the cell-based simulation state.

If SaveInterval (see [Time](#_group__ML__Time)) is specified, cell
states are automatically written to this element in the checkpointing
files (xml.gz).

This includes:

-   **Center:** cell center, center of mass, just informative

-   **Nodes:** list of lattice nodes occupied by the cell (lattice
    coordinates!)

-   **PropertyData:** value of a [Property](#_group__ML__Property)
    symbol

-   **PropertyVectorData:** x,y,z values of a
    [PropertyVector](#_group__ML__PropertyVector) symbol

-   **DelayPropertyData:** history of values of a
    [DelayProperty](#_group__ML__DelayProperty) symbol

-   **MembranePropertyData:** current values of the scalar field of a
    [MembraneProperty](#_group__ML__MembraneProperty)

Note, this element is not meant for manual specification by humans.

# ClusteringTracker {#_group__ML__ClusteringTracker}

ClusteringTracker

Identifies and writes distribution of cell clusters within a single
celltype.

Identifies and writes distribution of cell clusters within a single
celltype.

## Description {#_group__LengthConstraint_1Description}

ClusteringTracker identifies cell clusters within a single celltype and
writes the size distribution of cell clusters to a file.

A cell is considered part of a cluster if it at shares least 1 shares
interface (side of a lattice node) with it.

-   **time-step**: interval in which analysis is executed

-   **celltype:** comma separated list of cell types for which to detect
    cell clusters

-   **exclude** (optional): expression determining which cells to
    exclude

The cluster ID of each cell can be written to a symbol (preferrably a
cell property) to use in other postprocessing/visualisation steps.

-   **ClusterID/symbol-ref**: symbol (e.g.
    [Property](#_group__ML__Property)) to assign the current clusterID.

## Example {#_group__ML__Function_1Example}

Every 100 time-steps, write cluster size distribution to file:

        <ClusteringTracker time-step="100" celltype="CellType1">
        </ClusteringTracker>

Write cluster size distribution to file AND assign cluster ID to each
cell (assuming \'clusID\' is a cell [Property](#_classProperty)):

        <ClusteringTracker time-step="100" celltype="CellType1">
            <ClusterID symbol-ref="clusID" />
        </ClusteringTracker>

# ConstantVector {#_group__ML__ConstantVector}

ConstantVector

Symbol with a fixed 3D vector value, given by a
[MathExpressions](#_group__MathExpressions).

Syntax is comma-separated as given by **notation** : orthogonal - x,y,z
radial - r,φ,θ or radial - φ,θ,r

# Constant {#_group__ML__Constant}

Constant

Symbol with a fixed scalar value given by a
[MathExpressions](#_group__MathExpressions).

# Contact {#_group__ML__Contact}

Contact

Inter-celltype contact energies per length unit as defined in
[CPM](#_group__ML__CPM) ShapeSurface. Contact energies can be constant
values or expressions of global symbols or symbols of the involved cell
types.

## Modules {.unnumbered}

-   [AddOnAdhesion](#_group__ML__AddOnAdhesion)

    Additive interaction energy based on a global expression
    (deprecated)

-   [Constant](#_group__ML__Constant)

-   [Function](#_group__ML__Function)

    Parametric Function declaration.

-   [HeterophilicAdhesion](#_group__ML__HeterophilicAdhesion)

    Heterophilic adhesive interaction between neighboring CPM cells.

-   [HomophilicAdhesion](#_group__ML__HomophilicAdhesion)

    Homophilic adhesive interaction between neighboring CPM cells.