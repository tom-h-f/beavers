import gridworld as env
import render


def main():
    width = 128
    height = 128
    e = env.Environment(width, height)
    running = True
    try:
        gpu = render.PygameRenderer(width, height)

        while running:
            e.step()
            running = gpu.render(e)
    except KeyboardInterrupt:
        print("Exiting...")


if __name__ == "__main__":
    main()
