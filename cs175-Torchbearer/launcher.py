# launcher.py: responsible for mission startup and execution
from __future__ import print_function
import sys, time
import MalmoPython
from tensorboardX import SummaryWriter
from mission import GetMissionXML
from agent import run_episode
from constants import EPISODES, SCALE_FACTOR, EPSILON_START, EPSILON_END, EPSILON_DECAY
from qt_viz import init_canvas

def run():
    agent_host = MalmoPython.AgentHost()
    try:
        agent_host.parse(sys.argv)
    except RuntimeError as e:
        print("ERROR:", e)
        print(agent_host.getUsage())
        sys.exit(1)
    writer = SummaryWriter(log_dir="runs/dqn_smaller")
    ws = agent_host.getWorldState()
    canvas_host, canvas = init_canvas()

    epsilon = EPSILON_START
    for ep in range(1, EPISODES + 1):
        print("\n===== Starting Episode {} =====".format(ep))
        
        # Build the world and agent
        mission = MalmoPython.MissionSpec(GetMissionXML(), True)
        mission.requestVideo(1200, 900)
        #mission.setViewpoint(1)
        record  = MalmoPython.MissionRecordSpec()
        mission.removeAllCommandHandlers()
        mission.allowAllDiscreteMovementCommands()
        mission.allowAllChatCommands()
        mission.allowAbsoluteMovementCommand("tpx")
        mission.allowAbsoluteMovementCommand("tpy")
        mission.allowAbsoluteMovementCommand("tpz")

        # Start a new mission
        for attempt in range(3):
            try:
                agent_host.startMission(mission, record)
                break
            except RuntimeError as e:
                if attempt == 2:
                    print("Mission start failed:", e)
                    exit(1)
                time.sleep(1)

        # Wait for mission to start
        print("Waiting for mission to start", end="")
        ws = agent_host.getWorldState()
        while not ws.has_mission_begun:
            print(".", end="")
            time.sleep(0.1/SCALE_FACTOR)
            ws = agent_host.getWorldState()
            for error in ws.errors:
                print("Mission Error:", error.text)
        print("\nMission running!")

        # Run the episode
        reward = run_episode(agent_host, ep, writer, canvas=canvas, epsilon=epsilon)
        epsilon = max(EPSILON_END, epsilon * EPSILON_DECAY)
        print("[Episode {}] Reward = {:.2f}".format(ep, reward))

        while agent_host.getWorldState().is_mission_running:
            time.sleep(0.1)


    print("Done!")
    writer.flush()
    writer.close()
    time.sleep(1)
    

if __name__ == "__main__":
    run()
    