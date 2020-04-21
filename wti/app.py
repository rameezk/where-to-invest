from wti.simulator import Simulator
import wti.conf as conf


def main():
    simulator = Simulator(conf.age, conf.monthly_amount_to_invest)

    x = input("Press [q] to quit, any key to continue: ")
    while x != "q":
        simulator.run_one_month()
        summary = simulator.get_summary()

        print("=======================================")
        print(f"year = {summary.get('year_count')}")
        print(f"month = {summary.get('month_count')}")
        print(f"total_portfolio = {summary.get('total_portfolio'):.2f}")

        x = input("Press [q] to quit, any key to continue: ")


if __name__ == "__main__":
    main()
