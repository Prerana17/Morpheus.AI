<?xml version='1.0' encoding='UTF-8'?>
<MorpheusModel version="4">
    <Description>
        <Details></Details>
        <Title>AI</Title>
    </Description>
    <Space>
        <Lattice class="square">
            <Neighborhood>
                <Order>optimal</Order>
            </Neighborhood>
            <Size symbol="size" value="100.0, 100.0, 0.0"/>
            <BoundaryConditions>
                <Condition type="periodic" boundary="x"/>
                <Condition type="periodic" boundary="y"/>
            </BoundaryConditions>
        </Lattice>
        <SpaceSymbol symbol="space"/>
    </Space>
    <Time>
        <StartTime value="0"/>
        <StopTime value="1000"/>
        <TimeSymbol symbol="time"/>
    </Time>
    <Analysis>
        <ModelGraph include-tags="#untagged" format="dot" reduced="false"/>
        <Gnuplotter time-step="100">
            <Plot>
                <Cells value="cell.type"/>
            </Plot>
            <Terminal name="png"/>
        </Gnuplotter>
    </Analysis>
    <Global>
        <Constant symbol="parameter" value="1.0"/>
        <Constant symbol="temperature" value="20.0"/>
        <Field symbol="concentration" value="0.0"/>
    </Global>
    <CellTypes>
        <CellType name="cell" class="biological">
            <VolumeConstraint target="100" strength="1"/>
            <SurfaceConstraint target="1" strength="1" mode="aspherity"/>
        </CellType>
    </CellTypes>
    <CPM>
        <Interaction>
            <Contact type2="cell" type1="cell" value="10.0"/>
        </Interaction>
        <ShapeSurface scaling="norm">
            <Neighborhood>
                <Order>optimal</Order>
            </Neighborhood>
        </ShapeSurface>
        <MonteCarloSampler stepper="edgelist">
            <MCSDuration value="1"/>
            <MetropolisKinetics temperature="temperature"/>
            <Neighborhood>
                <Order>optimal</Order>
            </Neighborhood>
        </MonteCarloSampler>
    </CPM>
    <CellPopulations>
        <Population type="cell" name="cell" size="1">
            <InitCircle mode="regular" number-of-cells="10">
                <Dimensions center="size.x/2, size.y/2, 0.0" radius="size.x/2"/>
            </InitCircle>
        </Population>
    </CellPopulations>
</MorpheusModel>
