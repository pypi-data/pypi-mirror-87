from penvy.PenvyConfig import PenvyConfig
from penvy.container.dicontainer import Container
from penvy.env.EnvInitRunner import EnvInitRunner


def main():
    runner = EnvInitRunner([PenvyConfig()], Container)
    runner.run()


if __name__ == "__main__":
    main()
