import sim
import sys






def main():
    width = 128
    height = 128
    s = sim.Simulator(width, height)
    running = True
    try:
        s.run(running)
    except KeyboardInterrupt:
        print('Exiting...')



if __name__ == "__main__":
    main()
