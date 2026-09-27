# mission.py: generate mission XML
from constants import Y_FLOOR, X_LEFT_WALL, X_RIGHT_WALL, X_MID, Z_MIN, RUNTIME, TURNS, MS_PER_TICK

def get_mission_XML():
    # Format and Return
    return __generate_mission_XML().format(ms_per_tick=MS_PER_TICK,
        generate_curving_maze=__generate_curving_maze(turns=TURNS),
        yfloor_1=Y_FLOOR + 1,
        yfloor=Y_FLOOR,
        left_wall=X_LEFT_WALL,
        right_wall=X_RIGHT_WALL,
        xmid=X_MID,
        zStart=Z_MIN,
        yfloor_6=Y_FLOOR + 6,
        yfloor_5=Y_FLOOR + 5,
        yfloor_m1=Y_FLOOR - 1,
        tm=RUNTIME * 1000
    )

def GetMissionXML():
    return '''<?xml version="1.0" encoding="UTF-8" ?>
        <Mission xmlns="http://ProjectMalmo.microsoft.com"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <About><Summary>13x50 Corridor with 4 Forks</Summary></About>
            <ModSettings>
                <MsPerTick>{ms_per_tick}</MsPerTick>
            </ModSettings>
      <ServerSection>
        <ServerInitialConditions>
          <AllowSpawning>false</AllowSpawning>
          <Time>
              <StartTime>6000</StartTime>
              <AllowPassageOfTime>false</AllowPassageOfTime>
          </Time> 
          <Weather>clear</Weather>
        </ServerInitialConditions>
        <ServerHandlers>
          <FlatWorldGenerator generatorString="3;1*minecraft:bedrock,1*minecraft:dirt,1*minecraft:grass;1;"/>
          <DrawingDecorator>
            <DrawCuboid x1="100" y1="100" z1="100" x2="107" y2="100" z2="130" type="cobblestone"/>
            <DrawCuboid x1="100" y1="101" z1="100" x2="107" y2="101" z2="130" type="cobblestone"/>
            <DrawCuboid x1="100" y1="101" z1="100" x2="100" y2="106" z2="130" type="cobblestone"/>
            <DrawCuboid x1="108" y1="101" z1="100" x2="108" y2="106" z2="130" type="cobblestone"/>
            <DrawCuboid x1="101" y1="101" z1="100" x2="107" y2="106" z2="100" type="cobblestone"/>
            <DrawCuboid x1="101" y1="101" z1="128" x2="107" y2="101" z2="130" type="lapis_block"/>
            <DrawBlock x="107" y="102" z="105" type="web"/>
            <DrawBlock x="101" y="102" z="106" type="web"/>
            <DrawBlock x="106" y="102" z="109" type="web"/>
            <DrawBlock x="101" y="102" z="110" type="web"/>
            <DrawBlock x="103" y="102" z="114" type="web"/>
            <DrawBlock x="105" y="102" z="117" type="web"/>
            <DrawBlock x="102" y="102" z="123" type="web"/>
            <DrawBlock x="101" y="102" z="120" type="web"/>
            <DrawBlock x="104" y="101" z="107" type="water"/>
            <DrawBlock x="105" y="101" z="111" type="water"/>
            <DrawBlock x="101" y="101" z="117" type="water"/>
            <DrawBlock x="104" y="101" z="121" type="water"/>
            <DrawBlock x="106" y="101" z="123" type="water"/>
          </DrawingDecorator>
          <ServerQuitFromTimeUp timeLimitMs="30000"/>
          <ServerQuitWhenAnyAgentFinishes/>
        </ServerHandlers>
      </ServerSection>
      <AgentSection mode="Creative">
        <Name>QLearner</Name>
        <AgentStart>
          <Placement x="103.5" y="102.0" z="101.5" pitch="0" yaw="0"/>
        </AgentStart>
        <AgentHandlers>
          <DiscreteMovementCommands/>
          <AbsoluteMovementCommands/>
          <AgentQuitFromTouchingBlockType>
                <Block type="lapis_block"/>
          </AgentQuitFromTouchingBlockType>
          <ObservationFromFullStats/>
            <ObservationFromGrid>
                <Grid name="playergrid">
                    <min x="0" y="-1" z="0"/>
                    <max x="0" y="2" z="0"/>
                </Grid>
            </ObservationFromGrid>
        </AgentHandlers>
      </AgentSection>
    </Mission>'''.format(ms_per_tick=MS_PER_TICK).format(ms_per_tick=MS_PER_TICK)

def __generate_curving_maze(turns, gap_width=6):
    xml_parts = []
    wall_height = 6
    start_y = 179
    start_x = 112
    curving_maze_zmin = Z_MIN + 100  # 200
    for i, turn in enumerate(turns):
        z = curving_maze_zmin + i
        left_x = start_x + turn
        right_x = left_x + gap_width + 1  

        # Left wall
        xml_parts.append(
            '<DrawCuboid x1="{x}" y1="{y1}" z1="{z}" '
            'x2="{x}" y2="{y2}" z2="{z}" type="glass"/>'.format(
                x=left_x,
                y1=start_y,
                y2=start_y + wall_height - 1,
                z=z
            )
        )

        # Right wall
        xml_parts.append(
            '<DrawCuboid x1="{x}" y1="{y1}" z1="{z}" '
            'x2="{x}" y2="{y2}" z2="{z}" type="glass"/>'.format(
                x=right_x,
                y1=start_y,
                y2=start_y + wall_height - 1,
                z=z
            )
        )

        # Floor (from left_x to right_x, at y = floor level)
        xml_parts.append(
            '<DrawCuboid x1="{x1}" y1="{y}" z1="{z}" '
            'x2="{x2}" y2="{y}" z2="{z}" type="stone"/>'.format(
                x1=left_x,
                x2=right_x,
                y=start_y - 1,
                z=z
            )
        )

    return "\n".join(xml_parts)


def __generate_mission_XML():
    mission_header = '''
    <?xml version="1.0" encoding="UTF-8" ?>
    <Mission
        xmlns="http://ProjectMalmo.microsoft.com"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <About>
            <Summary>Corridor Section with Obsidian Walls & Glass Partition</Summary>
        </About>
        <ModSettings>
            <MsPerTick>{ms_per_tick}</MsPerTick>
        </ModSettings>
    '''
    agent_section = '''
        <AgentSection mode="Creative">
            <Name>SectionAgent</Name>
            <AgentStart>
                <!-- Agent Starting Point: (121,176,151) -->
                <Placement x="121.5" y="177" z="101" pitch="0" yaw="0"/>
            </AgentStart>
            <AgentHandlers>
                <VideoProducer>
                    <Width>1600</Width>
                    <Height>900</Height>
                </VideoProducer>
                <ContinuousMovementCommands/>
                <ObservationFromFullStats/>
                <AgentQuitFromTouchingBlockType>
                  <Block type="lava" />
                  <!-- Block type="water" / -->
                </AgentQuitFromTouchingBlockType>
            </AgentHandlers>
        </AgentSection>
    '''
    server_initializer = '''
        <ServerSection>
            <ServerInitialConditions>
                <Time>
                    <StartTime>1000</StartTime>
                    <!-- 6 AM -->
                    <AllowPassageOfTime>false</AllowPassageOfTime>
                    <!-- Set time -->
                </Time>
                <AllowSpawning>true</AllowSpawning>
            </ServerInitialConditions>
            <ServerHandlers>
                <FlatWorldGenerator generatorString="3;1*minecraft:bedrock,1*minecraft:dirt,1*minecraft:grass;1;"/>
                <DrawingDecorator>
    '''
    server_draw_base = '''
                    <DrawCuboid x1="{left_wall}" y1="{yfloor}" z1="{zStart}" x2="{right_wall}" y2="{yfloor_6}" z2="{zStart}" type="cobblestone_wall"/>
                    <DrawCuboid x1="{left_wall}" y1="{yfloor}" z1="{zStart}" x2="{left_wall}" y2="{yfloor_6}" z2="151" type="cobblestone_wall"/>
                    <DrawCuboid x1="{right_wall}" y1="{yfloor}" z1="{zStart}" x2="{right_wall}" y2="{yfloor_6}" z2="151" type="cobblestone_wall"/>
                    
                    <!-- Base Floor -->
                    <DrawCuboid x1="{left_wall}" y1="{yfloor}" z1="100" x2="{right_wall}" y2="{yfloor}" z2="106" type="glowstone"/>
                    <DrawCuboid x1="{left_wall}" y1="{yfloor}" z1="107" x2="{right_wall}" y2="{yfloor}" z2="152" type="glowstone"/>

                    <!-- Middle Wall 1 (glass) -->
                    <DrawCuboid x1="{xmid}" y1="{yfloor}" z1="155" x2="{xmid}" y2="{yfloor_5}" z2="195" type="glass"/>
                    <!-- Middle Wall 2 (glass) -->
                    <DrawCuboid x1="{xmid}" y1="{yfloor}" z1="200" x2="{xmid}" y2="{yfloor_5}" z2="299" type="glass"/>
                    
                    <!-- Starting point marker -->
                    <DrawBlock  x="{xmid}" y="{yfloor}" z="101" type="lapis_block"/>
    '''
    server_draw_pond_and_waterlily_stage = '''
                    <!-- Floor under the pond -->
                    <DrawCuboid x1="{left_wall}" y1="{yfloor_m1}" z1="106" x2="{right_wall}" y2="{yfloor_m1}" z2="151" type="glowstone"/>
                    <!-- Pond (water) -->
                    <DrawCuboid x1="116" y1="{yfloor}" z1="107" x2="126" y2="{yfloor}" z2="150" type="water"/>
                    
                    <!-- Waterlilly -->
                    <DrawBlock x="124" y="{yfloor_1}" z="107" type="waterlily"/>
                    <DrawBlock x="123" y="{yfloor_1}" z="107" type="waterlily"/>
                    <DrawBlock x="122" y="{yfloor_1}" z="107" type="waterlily"/>
                    <DrawBlock x="121" y="{yfloor_1}" z="107" type="waterlily"/>
                    <DrawBlock x="120" y="{yfloor_1}" z="107" type="waterlily"/>
                    <DrawBlock x="119" y="{yfloor_1}" z="107" type="waterlily"/>
                    <DrawBlock x="124" y="{yfloor_1}" z="107" type="waterlily"/>
                    <DrawBlock x="125" y="{yfloor_1}" z="108" type="waterlily"/>
                    <DrawBlock x="124" y="{yfloor_1}" z="108" type="waterlily"/>
                    <DrawBlock x="123" y="{yfloor_1}" z="108" type="waterlily"/>
                    <DrawBlock x="119" y="{yfloor_1}" z="108" type="waterlily"/>
                    <DrawBlock x="118" y="{yfloor_1}" z="108" type="waterlily"/>
                    <DrawBlock x="117" y="{yfloor_1}" z="108" type="waterlily"/>
                    <DrawBlock x="125" y="{yfloor_1}" z="109" type="waterlily"/>
                    <DrawBlock x="124" y="{yfloor_1}" z="109" type="waterlily"/>
                    <DrawBlock x="118" y="{yfloor_1}" z="109" type="waterlily"/>
                    <DrawBlock x="117" y="{yfloor_1}" z="109" type="waterlily"/>
                    <DrawBlock x="117" y="{yfloor_1}" z="110" type="waterlily"/>
                    <DrawBlock x="117" y="{yfloor_1}" z="110" type="waterlily"/>
                    <DrawBlock x="121" y="{yfloor_1}" z="109" type="waterlily"/>
                    <DrawBlock x="123" y="{yfloor_1}" z="111" type="waterlily"/>
                    <DrawBlock x="122" y="{yfloor_1}" z="111" type="waterlily"/>
                    <DrawBlock x="121" y="{yfloor_1}" z="111" type="waterlily"/>
                    <DrawBlock x="120" y="{yfloor_1}" z="111" type="waterlily"/>
                    <DrawBlock x="119" y="{yfloor_1}" z="111" type="waterlily"/>
                    <DrawBlock x="124" y="{yfloor_1}" z="118" type="waterlily"/>
                    <DrawBlock x="123" y="{yfloor_1}" z="118" type="waterlily"/>
                    <DrawBlock x="122" y="{yfloor_1}" z="118" type="waterlily"/>
                    <DrawBlock x="121" y="{yfloor_1}" z="119" type="waterlily"/>
                    <DrawBlock x="120" y="{yfloor_1}" z="120" type="waterlily"/>
                    <DrawBlock x="120" y="{yfloor_1}" z="121" type="waterlily"/>
                    <DrawBlock x="121" y="{yfloor_1}" z="122" type="waterlily"/>
                    <DrawBlock x="122" y="{yfloor_1}" z="122" type="waterlily"/>
                    <DrawBlock x="123" y="{yfloor_1}" z="123" type="waterlily"/>
                    <DrawBlock x="124" y="{yfloor_1}" z="123" type="waterlily"/>
                    <DrawBlock x="124" y="{yfloor_1}" z="124" type="waterlily"/>
                    <DrawBlock x="124" y="{yfloor_1}" z="125" type="waterlily"/>
                    <DrawBlock x="123" y="{yfloor_1}" z="125" type="waterlily"/>
                    <DrawBlock x="122" y="{yfloor_1}" z="125" type="waterlily"/>
                    <DrawBlock x="121" y="{yfloor_1}" z="125" type="waterlily"/>
                    <DrawBlock x="120" y="{yfloor_1}" z="125" type="waterlily"/>
                    <DrawBlock x="126" y="{yfloor_1}" z="127" type="waterlily"/>
                    <DrawBlock x="125" y="{yfloor_1}" z="127" type="waterlily"/>
                    <DrawBlock x="124" y="{yfloor_1}" z="127" type="waterlily"/>
                    <DrawBlock x="123" y="{yfloor_1}" z="127" type="waterlily"/>
                    <DrawBlock x="122" y="{yfloor_1}" z="127" type="waterlily"/>
                    <DrawBlock x="121" y="{yfloor_1}" z="127" type="waterlily"/>
                    <DrawBlock x="120" y="{yfloor_1}" z="127" type="waterlily"/>
                    <DrawBlock x="123" y="{yfloor_1}" z="128" type="waterlily"/>
                    <DrawBlock x="123" y="{yfloor_1}" z="129" type="waterlily"/>
                    <DrawBlock x="123" y="{yfloor_1}" z="130" type="waterlily"/>
                    <DrawBlock x="123" y="{yfloor_1}" z="131" type="waterlily"/>
                    <DrawBlock x="123" y="{yfloor_1}" z="132" type="waterlily"/>
                    <DrawBlock x="123" y="{yfloor_1}" z="133" type="waterlily"/>
                    <DrawBlock x="124" y="{yfloor_1}" z="132" type="waterlily"/>
                    <DrawBlock x="125" y="{yfloor_1}" z="131" type="waterlily"/>
                    <DrawBlock x="117" y="{yfloor_1}" z="118" type="waterlily"/>
                    <DrawBlock x="117" y="{yfloor_1}" z="119" type="waterlily"/>
                    <DrawBlock x="117" y="{yfloor_1}" z="120" type="waterlily"/>
                    <DrawBlock x="117" y="{yfloor_1}" z="121" type="waterlily"/>
                    <DrawBlock x="117" y="{yfloor_1}" z="122" type="waterlily"/>
                    <DrawBlock x="117" y="{yfloor_1}" z="123" type="waterlily"/>
                    <DrawBlock x="117" y="{yfloor_1}" z="124" type="waterlily"/>
                    <DrawBlock x="117" y="{yfloor_1}" z="125" type="waterlily"/>
                    <DrawBlock x="117" y="{yfloor_1}" z="126" type="waterlily"/>
                    <DrawBlock x="117" y="{yfloor_1}" z="127" type="waterlily"/>
                    <DrawBlock x="117" y="{yfloor_1}" z="128" type="waterlily"/>
                    <DrawBlock x="117" y="{yfloor_1}" z="129" type="waterlily"/>
                    <DrawBlock x="117" y="{yfloor_1}" z="130" type="waterlily"/>
                    <DrawBlock x="117" y="{yfloor_1}" z="131" type="waterlily"/>
                    <DrawBlock x="118" y="{yfloor_1}" z="131" type="waterlily"/>
                    <DrawBlock x="119" y="{yfloor_1}" z="131" type="waterlily"/>
                    <DrawBlock x="120" y="{yfloor_1}" z="131" type="waterlily"/>
                    <DrawBlock x="121" y="{yfloor_1}" z="131" type="waterlily"/>
                    <DrawBlock x="121" y="{yfloor_1}" z="130" type="waterlily"/>
                    <DrawBlock x="121" y="{yfloor_1}" z="129" type="waterlily"/>
                    <DrawBlock x="122" y="{yfloor_1}" z="134" type="waterlily"/>
                    <DrawBlock x="121" y="{yfloor_1}" z="134" type="waterlily"/>
                    <DrawBlock x="120" y="{yfloor_1}" z="134" type="waterlily"/>
                    <DrawBlock x="119" y="{yfloor_1}" z="134" type="waterlily"/>
                    <DrawBlock x="118" y="{yfloor_1}" z="135" type="waterlily"/>
                    <DrawBlock x="118" y="{yfloor_1}" z="136" type="waterlily"/>
                    <DrawBlock x="119" y="{yfloor_1}" z="137" type="waterlily"/>
                    <DrawBlock x="120" y="{yfloor_1}" z="138" type="waterlily"/>
                    <DrawBlock x="121" y="{yfloor_1}" z="139" type="waterlily"/>
                    <DrawBlock x="121" y="{yfloor_1}" z="140" type="waterlily"/>
                    <DrawBlock x="120" y="{yfloor_1}" z="141" type="waterlily"/>
                    <DrawBlock x="119" y="{yfloor_1}" z="141" type="waterlily"/>
                    <DrawBlock x="118" y="{yfloor_1}" z="141" type="waterlily"/>
                    <DrawBlock x="117" y="{yfloor_1}" z="141" type="waterlily"/>
                    <DrawBlock x="120" y="{yfloor_1}" z="143" type="waterlily"/>
                    <DrawBlock x="121" y="{yfloor_1}" z="143" type="waterlily"/>
                    <DrawBlock x="122" y="{yfloor_1}" z="143" type="waterlily"/>
                    <DrawBlock x="123" y="{yfloor_1}" z="143" type="waterlily"/>
                    <DrawBlock x="124" y="{yfloor_1}" z="144" type="waterlily"/>
                    <DrawBlock x="125" y="{yfloor_1}" z="145" type="waterlily"/>
                    <DrawBlock x="125" y="{yfloor_1}" z="146" type="waterlily"/>
                    <DrawBlock x="125" y="{yfloor_1}" z="147" type="waterlily"/>
                    <DrawBlock x="124" y="{yfloor_1}" z="148" type="waterlily"/>
                    <DrawBlock x="123" y="{yfloor_1}" z="149" type="waterlily"/>
                    <DrawBlock x="122" y="{yfloor_1}" z="149" type="waterlily"/>
                    <DrawBlock x="121" y="{yfloor_1}" z="149" type="waterlily"/>
                    <DrawBlock x="120" y="{yfloor_1}" z="149" type="waterlily"/>
                    <DrawBlock x="122" y="{yfloor_1}" z="110" type="waterlily"/>
                    <DrawBlock x="121" y="{yfloor_1}" z="110" type="waterlily"/>
                    <DrawBlock x="120" y="{yfloor_1}" z="110" type="waterlily"/>
                    <DrawBlock x="124" y="{yfloor_1}" z="112" type="waterlily"/>
                    <DrawBlock x="123" y="{yfloor_1}" z="112" type="waterlily"/>
                    <DrawBlock x="122" y="{yfloor_1}" z="112" type="waterlily"/>
                    <DrawBlock x="121" y="{yfloor_1}" z="112" type="waterlily"/>
                    <DrawBlock x="120" y="{yfloor_1}" z="112" type="waterlily"/>
                    <DrawBlock x="119" y="{yfloor_1}" z="112" type="waterlily"/>
                    <DrawBlock x="118" y="{yfloor_1}" z="112" type="waterlily"/>
                    <DrawBlock x="125" y="{yfloor_1}" z="113" type="waterlily"/>
                    <DrawBlock x="124" y="{yfloor_1}" z="113" type="waterlily"/>
                    <DrawBlock x="123" y="{yfloor_1}" z="113" type="waterlily"/>
                    <DrawBlock x="122" y="{yfloor_1}" z="113" type="waterlily"/>
                    <DrawBlock x="121" y="{yfloor_1}" z="113" type="waterlily"/>
                    <DrawBlock x="120" y="{yfloor_1}" z="113" type="waterlily"/>
                    <DrawBlock x="119" y="{yfloor_1}" z="113" type="waterlily"/>
                    <DrawBlock x="118" y="{yfloor_1}" z="113" type="waterlily"/>
                    <DrawBlock x="117" y="{yfloor_1}" z="113" type="waterlily"/>
                    <DrawBlock x="126" y="{yfloor_1}" z="114" type="waterlily"/>
                    <DrawBlock x="125" y="{yfloor_1}" z="114" type="waterlily"/>
                    <DrawBlock x="124" y="{yfloor_1}" z="114" type="waterlily"/>
                    <DrawBlock x="123" y="{yfloor_1}" z="114" type="waterlily"/>
                    <DrawBlock x="122" y="{yfloor_1}" z="114" type="waterlily"/>
                    <DrawBlock x="120" y="{yfloor_1}" z="114" type="waterlily"/>
                    <DrawBlock x="119" y="{yfloor_1}" z="114" type="waterlily"/>
                    <DrawBlock x="118" y="{yfloor_1}" z="114" type="waterlily"/>
                    <DrawBlock x="117" y="{yfloor_1}" z="114" type="waterlily"/>
                    <DrawBlock x="116" y="{yfloor_1}" z="114" type="waterlily"/>
                    <DrawBlock x="125" y="{yfloor_1}" z="115" type="waterlily"/>
                    <DrawBlock x="124" y="{yfloor_1}" z="115" type="waterlily"/>
                    <DrawBlock x="123" y="{yfloor_1}" z="115" type="waterlily"/>
                    <DrawBlock x="122" y="{yfloor_1}" z="115" type="waterlily"/>
                    <DrawBlock x="119" y="{yfloor_1}" z="115" type="waterlily"/>
                    <DrawBlock x="118" y="{yfloor_1}" z="115" type="waterlily"/>
                    <DrawBlock x="117" y="{yfloor_1}" z="115" type="waterlily"/>
                    <DrawBlock x="116" y="{yfloor_1}" z="115" type="waterlily"/>
                    <DrawBlock x="125" y="{yfloor_1}" z="116" type="waterlily"/>
                    <DrawBlock x="124" y="{yfloor_1}" z="116" type="waterlily"/>
                    <DrawBlock x="118" y="{yfloor_1}" z="116" type="waterlily"/>
                    <DrawBlock x="117" y="{yfloor_1}" z="116" type="waterlily"/>    
    '''
    server_draw_obsidian_stage = '''
                    <!-- Floor (Stone) -->
                    <DrawCuboid x1="{left_wall}" y1="{yfloor}" z1="151" x2="{right_wall}" y2="{yfloor}" z2="196" type="stone"/>
                    <!-- Side Walls (Obsidian) -->
                    <DrawCuboid x1="{left_wall}" y1="{yfloor}" z1="151" x2="{left_wall}" y2="186" z2="196" type="obsidian"/>
                    <DrawCuboid x1="{right_wall}" y1="{yfloor}" z1="151" x2="{right_wall}" y2="186" z2="196" type="obsidian"/>
                    <!-- Middle Wall (Glass) -->
                    <DrawCuboid x1="{xmid}" y1="{yfloor}" z1="155" x2="{xmid}" y2="186" z2="196" type="glass"/>
                    <!-- Right water pit & Glowstone walkway -->
                    <DrawCuboid x1="116" y1="175" z1="164" x2="120" y2="175" z2="165" type="stone"/>
                    <DrawCuboid x1="116" y1="{yfloor}" z1="164" x2="120" y2="{yfloor}" z2="165" type="water"/>
                    <DrawBlock x="117" y="176" z="165" type="glowstone"/>
                    <DrawBlock x="118" y="176" z="164" type="glowstone"/>
                    <DrawBlock x="119" y="176" z="165" type="glowstone"/>
                    <!-- Left lava pit & Glowstone walkway -->
                    <DrawCuboid x1="122" y1="175" z1="164" x2="126" y2="175" z2="165" type="stone"/>
                    <DrawCuboid x1="122" y1="{yfloor}" z1="164" x2="126" y2="{yfloor}" z2="165" type="lava"/>
                    <DrawBlock x="123" y="176" z="165" type="glowstone"/>
                    <DrawBlock x="124" y="176" z="164" type="glowstone"/>
                    <DrawBlock x="125" y="176" z="165" type="glowstone"/>
                    <!-- Water and Stone at z=169 -->
                    <DrawBlock x="116" y="175" z="169" type="stone"/>
                    <DrawBlock x="116" y="{yfloor}" z="169" type="water"/>
                    <DrawBlock x="118" y="175" z="169" type="stone"/>
                    <DrawBlock x="118" y="{yfloor}" z="169" type="water"/>
                    <DrawBlock x="120" y="175" z="169" type="stone"/>
                    <DrawBlock x="120" y="{yfloor}" z="169" type="water"/>
                    <!-- Lava and Stone at z=169 -->
                    <DrawBlock x="122" y="175" z="169" type="stone"/>
                    <DrawBlock x="122" y="{yfloor}" z="169" type="lava"/>
                    <DrawBlock x="124" y="175" z="169" type="stone"/>
                    <DrawBlock x="124" y="{yfloor}" z="169" type="lava"/>
                    <DrawBlock x="126" y="175" z="169" type="stone"/>
                    <DrawBlock x="126" y="{yfloor}" z="169" type="lava"/>
                    <!-- Water and Stone at z=171~174 -->
                    <DrawBlock x="118" y="175" z="171" type="stone"/>
                    <DrawBlock x="118" y="{yfloor}" z="171" type="water"/>
                    <DrawCuboid x1="117" y1="175" z1="172" x2="117" y2="175" z2="174" type="stone"/>
                    <DrawCuboid x1="117" y1="{yfloor}" z1="172" x2="117" y2="{yfloor}" z2="174" type="water"/>
                    <!-- Lava and Stone at z=171~174 -->
                    <DrawBlock x="124" y="175" z="171" type="stone"/>
                    <DrawBlock x="124" y="{yfloor}" z="171" type="lava"/>
                    <DrawCuboid x1="125" y1="175" z1="172" x2="125" y2="175" z2="174" type="stone"/>
                    <DrawCuboid x1="125" y1="{yfloor}" z1="172" x2="125" y2="{yfloor}" z2="174" type="lava"/>
                    <!-- Water and Stone pit at z=180~187 -->
                    <DrawBlock x="117" y="175" z="180" type="stone"/>
                    <DrawBlock x="117" y="{yfloor}" z="180" type="water"/>
                    <DrawCuboid x1="116" y1="175" z1="181" x2="116" y2="175" z2="183" type="stone"/>
                    <DrawCuboid x1="116" y1="{yfloor}" z1="181" x2="116" y2="{yfloor}" z2="183" type="water"/>
                    <DrawBlock x="119" y="175" z="182" type="stone"/>
                    <DrawBlock x="119" y="{yfloor}" z="182" type="water"/>
                    <DrawBlock x="117" y="175" z="184" type="stone"/>
                    <DrawBlock x="117" y="{yfloor}" z="184" type="water"/>
                    <DrawBlock x="118" y="175" z="185" type="stone"/>
                    <DrawBlock x="118" y="{yfloor}" z="185" type="water"/>
                    <DrawBlock x="119" y="175" z="186" type="stone"/>
                    <DrawBlock x="119" y="{yfloor}" z="186" type="water"/>
                    <DrawBlock x="120" y="175" z="187" type="stone"/>
                    <DrawBlock x="120" y="{yfloor}" z="187" type="water"/>
                    <!-- Lava and stone pit at z=180~187 -->
                    <DrawBlock x="125" y="175" z="180" type="stone"/>
                    <DrawBlock x="125" y="{yfloor}" z="180" type="lava"/>
                    <DrawCuboid x1="126" y1="175" z1="181" x2="126" y2="175" z2="183" type="stone"/>
                    <DrawCuboid x1="126" y1="{yfloor}" z1="181" x2="126" y2="{yfloor}" z2="183" type="lava"/>
                    <DrawBlock x="123" y="175" z="182" type="stone"/>
                    <DrawBlock x="123" y="{yfloor}" z="182" type="lava"/>
                    <DrawBlock x="125" y="175" z="184" type="stone"/>
                    <DrawBlock x="125" y="{yfloor}" z="184" type="lava"/>
                    <DrawBlock x="124" y="175" z="185" type="stone"/>
                    <DrawBlock x="124" y="{yfloor}" z="185" type="lava"/>
                    <DrawBlock x="123" y="175" z="186" type="stone"/>
                    <DrawBlock x="123" y="{yfloor}" z="186" type="lava"/>
                    <DrawBlock x="122" y="175" z="187" type="stone"/>
                    <DrawBlock x="122" y="{yfloor}" z="187" type="lava"/>    
    '''
    server_draw_ladder_and_stairs = '''
                    <!-- Stone wall at x=116~120, y=176~177, z=196 -->
                    <DrawCuboid x1="116" y1="{yfloor}" z1="196" x2="120" y2="177" z2="196" type="stone"/>
                    <DrawCuboid x1="116" y1="177" z1="196" x2="120" y2="178" z2="196" type="stone"/>
                    <!-- Place ladder on stone wall on the right path -->
                    <DrawBlock x="116" y="177" z="195" type="ladder"/>
                    <DrawBlock x="117" y="177" z="195" type="ladder"/>
                    <DrawBlock x="118" y="177" z="195" type="ladder"/>
                    <DrawBlock x="119" y="177" z="195" type="ladder"/>
                    <DrawBlock x="120" y="177" z="195" type="ladder"/>
                    <DrawBlock x="116" y="178" z="195" type="ladder"/>
                    <DrawBlock x="117" y="178" z="195" type="ladder"/>
                    <DrawBlock x="118" y="178" z="195" type="ladder"/>
                    <DrawBlock x="119" y="178" z="195" type="ladder"/>
                    <DrawBlock x="120" y="178" z="195" type="ladder"/>
                    <DrawCuboid x1="122" y1="{yfloor}" z1="196" x2="126" y2="177" z2="196" type="stone"/>
                    <!-- Place Stone stairs on the left path -->
                    <DrawCuboid x1="122" y1="177" z1="195" x2="126" y2="177" z2="196" type="stone_stairs" face="SOUTH"/>
                    <DrawCuboid x1="122" y1="178" z1="196" x2="126" y2="178" z2="196" type="stone_stairs" face="SOUTH"/>    
    '''
    server_draw_curving_maze_stage = '''
                    <!-- Generate curving maze -->
                    {generate_curving_maze}
                    <!-- Middle wall at the fork -->
                    <DrawCuboid x1="120" y1="178" z1="200" x2="{xmid}" y2="184" z2="200" type="stone"/>
    '''
    server_draw_spider_web_stage = '''
                    <DrawCuboid x1="{xmid}" y1="179" z1="200" x2="{xmid}" y2="184" z2="299" type="glass"/>
                    <DrawCuboid x1="{right_wall}" y1="179" z1="200" x2="{right_wall}" y2="184" z2="299" type="glass"/>
                    <DrawBlock x="125" y="179" z="223" type="web"/>
                    <DrawCuboid x1="126" y1="179" z1="222" x2="126" y2="179" z2="224" type="web"/>
                    <DrawCuboid x1="122" y1="179" z1="228" x2="123" y2="179" z2="228" type="web"/>
                    <DrawCuboid x1="125" y1="179" z1="228" x2="126" y2="179" z2="228" type="web"/>
                    <DrawCuboid x1="124" y1="179" z1="231" x2="124" y2="179" z2="232" type="web"/>
                    <DrawCuboid x1="122" y1="179" z1="235" x2="123" y2="179" z2="235" type="web"/>
                    <DrawBlock x="125" y="179" z="235" type="web"/>
                    <DrawBlock x="123" y="179" z="238" type="web"/>
                    <DrawCuboid x1="125" y1="179" z1="238" x2="126" y2="179" z2="238" type="web"/>
                    <DrawCuboid x1="123" y1="179" z1="241" x2="125" y2="179" z2="242" type="web"/>
                    <DrawBlock x="124" y="179" z="243" type="web"/>
                    <DrawCuboid x1="123" y1="179" z1="244" x2="125" y2="179" z2="245" type="web"/>
                    <DrawBlock x="124" y="179" z="246" type="web"/>
                    <DrawCuboid x1="123" y1="179" z1="247" x2="125" y2="179" z2="248" type="web"/>
                    <DrawBlock x="123" y="179" z="253" type="web"/>
                    <DrawBlock x="125" y="179" z="253" type="web"/>
                    <DrawBlock x="123" y="170" z="255" type="web"/>
                    <DrawBlock x="125" y="179" z="255" type="web"/>
                    <DrawBlock x="122" y="179" z="254" type="web"/>
                    <DrawBlock x="126" y="179" z="254" type="web"/>
                    <DrawCuboid x1="122" y1="179" z1="282" x2="122" y2="179" z2="284" type="web"/>
                    <DrawCuboid x1="124" y1="179" z1="282" x2="126" y2="179" z2="284" type="web"/>
                    <DrawCuboid x1="124" y1="179" z1="270" x2="126" y2="179" z2="272" type="web"/>
                    <DrawCuboid x1="122" y1="179" z1="264" x2="124" y2="179" z2="266" type="web"/>
                    <DrawCuboid x1="{left_wall}" y1="179" z1="197" x2="{left_wall}" y2="184" z2="199" type="stone"/>
                    <DrawCuboid x1="{right_wall}" y1="179" z1="197" x2="{right_wall}" y2="184" z2="199" type="stone"/>
                    <DrawCuboid x1="{left_wall}" y1="178" z1="197" x2="{right_wall}" y2="178" z2="199" type="stone"/>
                    <DrawCuboid x1="{xmid}" y1="178" z1="200" x2="{right_wall}" y2="178" z2="299" type="stone"/>
                    <DrawCuboid x1="112" y1="178" z1="297" x2="119" y2="178" z2="299" type="stone"/>
                    <DrawCuboid x1="119" y1="178" z1="297" x2="119" y2="184" z2="299" type="glass"/>
                    <DrawCuboid x1="112" y1="178" z1="297" x2="112" y2="184" z2="299" type="glass"/>    
    '''
    server_draw_ending_water_pool = '''
                    <!-- Water Pool (End Point) -->
                    <DrawCuboid x1="90" y1="2" z1="274" x2="152" y2="2" z2="326" type="water"/>
                    
                    <!-- Message "CONGRATS!" -->
                    <!-- "C" -->
                    <DrawBlock x="143" y="9" z="370" type="glowstone"/>
                    <DrawBlock x="144" y="9" z="370" type="glowstone"/>
                    <DrawBlock x="145" y="9" z="370" type="glowstone"/>
                    <DrawBlock x="142" y="8" z="370" type="glowstone"/>
                    <DrawBlock x="146" y="8" z="370" type="glowstone"/>
                    <DrawBlock x="146" y="7" z="370" type="glowstone"/>
                    <DrawBlock x="142" y="6" z="370" type="glowstone"/>
                    <DrawBlock x="146" y="6" z="370" type="glowstone"/>
                    <DrawBlock x="143" y="5" z="370" type="glowstone"/>
                    <DrawBlock x="144" y="5" z="370" type="glowstone"/>
                    <DrawBlock x="145" y="5" z="370" type="glowstone"/>
                    <!-- "O" -->
                    <DrawBlock x="137" y="9" z="370" type="glowstone"/>
                    <DrawBlock x="138" y="9" z="370" type="glowstone"/>
                    <DrawBlock x="139" y="9" z="370" type="glowstone"/>
                    <DrawBlock x="136" y="8" z="370" type="glowstone"/>
                    <DrawBlock x="140" y="8" z="370" type="glowstone"/>
                    <DrawBlock x="136" y="7" z="370" type="glowstone"/>
                    <DrawBlock x="140" y="7" z="370" type="glowstone"/>
                    <DrawBlock x="136" y="6" z="370" type="glowstone"/>
                    <DrawBlock x="140" y="6" z="370" type="glowstone"/>
                    <DrawBlock x="137" y="5" z="370" type="glowstone"/>
                    <DrawBlock x="138" y="5" z="370" type="glowstone"/>
                    <DrawBlock x="139" y="5" z="370" type="glowstone"/>
                    <!-- "N" -->
                    <DrawBlock x="130" y="9" z="370" type="glowstone"/>
                    <DrawBlock x="134" y="9" z="370" type="glowstone"/>
                    <DrawBlock x="130" y="8" z="370" type="glowstone"/>
                    <DrawBlock x="133" y="8" z="370" type="glowstone"/>
                    <DrawBlock x="134" y="8" z="370" type="glowstone"/>
                    <DrawBlock x="130" y="7" z="370" type="glowstone"/>
                    <DrawBlock x="132" y="7" z="370" type="glowstone"/>
                    <DrawBlock x="134" y="7" z="370" type="glowstone"/>
                    <DrawBlock x="130" y="6" z="370" type="glowstone"/>
                    <DrawBlock x="131" y="6" z="370" type="glowstone"/>
                    <DrawBlock x="134" y="6" z="370" type="glowstone"/>
                    <DrawBlock x="130" y="5" z="370" type="glowstone"/>
                    <DrawBlock x="134" y="5" z="370" type="glowstone"/>
                    <!-- "G" -->
                    <DrawBlock x="125" y="9" z="370" type="glowstone"/>
                    <DrawBlock x="126" y="9" z="370" type="glowstone"/>
                    <DrawBlock x="127" y="9" z="370" type="glowstone"/>
                    <DrawBlock x="128" y="8" z="370" type="glowstone"/>
                    <DrawBlock x="124" y="7" z="370" type="glowstone"/>
                    <DrawBlock x="125" y="7" z="370" type="glowstone"/>
                    <DrawBlock x="128" y="7" z="370" type="glowstone"/>
                    <DrawBlock x="124" y="6" z="370" type="glowstone"/>
                    <DrawBlock x="128" y="6" z="370" type="glowstone"/>
                    <DrawBlock x="125" y="5" z="370" type="glowstone"/>
                    <DrawBlock x="126" y="5" z="370" type="glowstone"/>
                    <DrawBlock x="127" y="5" z="370" type="glowstone"/>
                    <!-- "R" -->
                    <DrawBlock x="120" y="9" z="370" type="glowstone"/>
                    <DrawBlock x="121" y="9" z="370" type="glowstone"/>
                    <DrawBlock x="122" y="9" z="370" type="glowstone"/>
                    <DrawBlock x="119" y="8" z="370" type="glowstone"/>
                    <DrawBlock x="122" y="8" z="370" type="glowstone"/>
                    <DrawBlock x="120" y="7" z="370" type="glowstone"/>
                    <DrawBlock x="121" y="7" z="370" type="glowstone"/>
                    <DrawBlock x="122" y="7" z="370" type="glowstone"/>
                    <DrawBlock x="120" y="6" z="370" type="glowstone"/>
                    <DrawBlock x="122" y="6" z="370" type="glowstone"/>
                    <DrawBlock x="119" y="5" z="370" type="glowstone"/>
                    <DrawBlock x="122" y="5" z="370" type="glowstone"/>
                    <!-- "A" -->
                    <DrawBlock x="114" y="9" z="370" type="glowstone"/>
                    <DrawBlock x="115" y="9" z="370" type="glowstone"/>
                    <DrawBlock x="116" y="9" z="370" type="glowstone"/>
                    <DrawBlock x="113" y="8" z="370" type="glowstone"/>
                    <DrawBlock x="117" y="8" z="370" type="glowstone"/>
                    <DrawBlock x="113" y="7" z="370" type="glowstone"/>
                    <DrawBlock x="114" y="7" z="370" type="glowstone"/>
                    <DrawBlock x="115" y="7" z="370" type="glowstone"/>
                    <DrawBlock x="116" y="7" z="370" type="glowstone"/>
                    <DrawBlock x="117" y="7" z="370" type="glowstone"/>
                    <DrawBlock x="113" y="6" z="370" type="glowstone"/>
                    <DrawBlock x="117" y="6" z="370" type="glowstone"/>
                    <DrawBlock x="113" y="5" z="370" type="glowstone"/>
                    <DrawBlock x="117" y="5" z="370" type="glowstone"/>
                    <!-- "T" -->
                    <DrawBlock x="107" y="9" z="370" type="glowstone"/>
                    <DrawBlock x="108" y="9" z="370" type="glowstone"/>
                    <DrawBlock x="109" y="9" z="370" type="glowstone"/>
                    <DrawBlock x="110" y="9" z="370" type="glowstone"/>
                    <DrawBlock x="111" y="9" z="370" type="glowstone"/>
                    <DrawBlock x="109" y="8" z="370" type="glowstone"/>
                    <DrawBlock x="109" y="7" z="370" type="glowstone"/>
                    <DrawBlock x="109" y="6" z="370" type="glowstone"/>
                    <DrawBlock x="109" y="5" z="370" type="glowstone"/>
                    <!-- "S" -->
                    <DrawBlock x="101" y="9" z="370" type="glowstone"/>
                    <DrawBlock x="102" y="9" z="370" type="glowstone"/>
                    <DrawBlock x="103" y="9" z="370" type="glowstone"/>
                    <DrawBlock x="104" y="9" z="370" type="glowstone"/>
                    <DrawBlock x="105" y="9" z="370" type="glowstone"/>
                    <DrawBlock x="105" y="8" z="370" type="glowstone"/>
                    <DrawBlock x="105" y="7" z="370" type="glowstone"/>
                    <DrawBlock x="101" y="7" z="370" type="glowstone"/>
                    <DrawBlock x="102" y="7" z="370" type="glowstone"/>
                    <DrawBlock x="103" y="7" z="370" type="glowstone"/>
                    <DrawBlock x="104" y="7" z="370" type="glowstone"/>
                    <DrawBlock x="101" y="6" z="370" type="glowstone"/>
                    <DrawBlock x="105" y="5" z="370" type="glowstone"/>
                    <DrawBlock x="101" y="5" z="370" type="glowstone"/>
                    <DrawBlock x="102" y="5" z="370" type="glowstone"/>
                    <DrawBlock x="103" y="5" z="370" type="glowstone"/>
                    <DrawBlock x="104" y="5" z="370" type="glowstone"/>
                    <!-- "!" -->
                    <DrawBlock x="98" y="9" z="370" type="glowstone"/>
                    <DrawBlock x="98" y="8" z="370" type="glowstone"/>
                    <DrawBlock x="98" y="7" z="370" type="glowstone"/>
                    <DrawBlock x="98" y="5" z="370" type="glowstone"/>
                    </DrawingDecorator>
                <ServerQuitFromTimeUp timeLimitMs="{tm}"/>
            </ServerHandlers>
        </ServerSection>
    '''
    mission_footer = '''     
    </Mission>    
    '''
    
    # Generate full XML string
    full_xml = (
        mission_header
        + server_initializer
        + server_draw_base
        + server_draw_pond_and_waterlily_stage
        + server_draw_obsidian_stage
        + server_draw_ladder_and_stairs
        + server_draw_curving_maze_stage
        + server_draw_spider_web_stage
        + server_draw_ending_water_pool
        + agent_section
        + mission_footer
    )

    return full_xml
    
    