from wti.simulator import Simulator
import wti.conf as conf


def main():
    simulator = Simulator(conf.age, conf.monthly_amount_to_invest)

    x = input("Press [q] to quit, any key to continue: ")
    while x != "q":
        simulator.run_one_month()
        print(simulator.get_summary())
        x = input("Press [q] to quit, any key to continue: ")


if __name__ == "__main__":
    main()
