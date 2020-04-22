from wti.simulator import Simulator
import wti.conf as conf
import logging

logging.basicConfig(level=conf.log_level)

_log = logging.getLogger(__name__)


def interative():
    simulator = Simulator(conf.age, conf.monthly_amount_to_invest)

    x = input("Press [q] to quit, any key to continue: ")
    while x != "q":
        simulator.run_one_month()
        summary = simulator.get_summary()

        print("=======================================")
        print(f"year = {summary.get('year_count')}")
        print(f"month = {summary.get('month_count')}")
        tfsa_balance = simulator.portfolio.get("tfsa").get("balance")
        offshore_balance = simulator.portfolio.get("offshore").get("balance")
        print(f"tfsa = {tfsa_balance:.2f}")
        print(f"offshore = {offshore_balance:.2f}")
        print(f"total_portfolio = {summary.get('total_portfolio'):.2f}")

        x = input("Press [q] to quit, any key to continue: ")


def when_will_portfolio_be():
    simulator = Simulator(conf.age, conf.monthly_amount_to_invest)
    x = float(input("Enter monthly FI amount to continue: "))
    amount = x * 12.0 * 25.0
    print(f"Target is {amount:.2f} in today's money")
    print(f"Monthly investment amount is {conf.monthly_amount_to_invest:.2f}")
    when = simulator.run_until_portfolio_is(amount)
    print(when)


if __name__ == "__main__":
    # interative()
    when_will_portfolio_be()
