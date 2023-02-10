# pylint: disable=W,C,R

import csv
import io


class Curve:
    bond_supply: int = 100

    def create_cost(self) -> int:
        return self.bond_supply  # rais

    def burn_payment(self) -> int:
        return self.bond_supply - 1  # rais

    def create_bond(self) -> int:
        cost = self.create_cost()
        self.bond_supply += 1
        return cost

    def burn_bond(self) -> int:
        payment = self.burn_payment()
        self.bond_supply -= 1
        return payment


class LendingMarket:
    bond: int = 100
    rai: int = 1000000
    curve: Curve

    def __init__(self, curve: Curve):
        self.curve = curve

    def borrow_rai(self, bond_amount: int) -> int:
        self.bond += bond_amount
        rai_amount = 0.75 * self.curve.create_cost() * bond_amount
        self.rai -= rai_amount
        return rai_amount


class Account:
    bond = 0
    rai = 10000
    bond_as_collateral = 0
    rai_which_is_debt = 0
    curve: Curve
    lending_market: LendingMarket

    STATUS_LINE_HEADERS = [
        "action",
        "RAI holdings",
        "RAI which is debt",
        "BOND holdings",
        "BOND as collateral",
        "BOND supply",
        "BOND in lending market",
        "RAI in lending market",
    ]

    def __init__(self, curve: Curve, lending_market: LendingMarket):
        self.curve = curve
        self.lending_market = lending_market

    def buy_max_bond(self) -> int:
        total_bought = 0
        while True:
            if self.curve.create_cost() > self.rai:
                break
            self.rai -= self.curve.create_bond()
            self.bond += 1
            total_bought += 1
        return total_bought

    def borrow_rai(self) -> int:
        borrowed = 0
        self.bond_as_collateral += self.bond
        self.bond = 0
        borrowed = self.lending_market.borrow_rai(self.bond_as_collateral)
        self.rai_which_is_debt += borrowed
        self.rai += borrowed
        return borrowed

    def status_line(self) -> [str]:
        return list(
            map(
                str,
                [
                    int(self.rai),
                    self.bond,
                    self.bond_as_collateral,
                    self.curve.bond_supply,
                    int(self.rai_which_is_debt),
                    self.lending_market.bond,
                    self.lending_market.rai,
                ],
            )
        )


def main():
    curve = Curve()
    lm = LendingMarket(curve)
    account = Account(curve, lm)
    output = io.StringIO()
    w = csv.writer(output)
    w.writerow(Account.STATUS_LINE_HEADERS)
    w.writerow(["Start"] + account.status_line())
    for _ in range(5):
        w.writerow([f"Bought {account.buy_max_bond()} BOND"] + account.status_line())
        w.writerow([(f"Borrowed {account.borrow_rai()} RAI")] + account.status_line())
    print(output.getvalue())

if __name__ == "__main__":
    main()
