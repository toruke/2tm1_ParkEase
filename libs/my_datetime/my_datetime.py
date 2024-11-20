from datetime import datetime
from calendar import monthrange


class MyDateTime(datetime):
    def add_months(self, months):
        new_month = (self.month - 1 + months) % 12 + 1
        new_year = self.year + (self.month - 1 + months) // 12

        try:
            return self.replace(year=new_year, month=new_month)
        except ValueError:
            last_day_of_month = monthrange(new_year, new_month)[1]
            return self.replace(year=new_year, month=new_month, day=last_day_of_month)
