# repositories/dashboard_repository.py

import calendar
from collections import defaultdict
from datetime import date
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.project_record import ProjectRecord


class DashboardRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_analytics(
        self,
        project_id: int,
        year: int,
        month: int,
    ) -> dict:
        """
        Get dashboard analytics for a project.

        Income is calculated from the parts recorded
        under each service.

        Formula:

            income = quantity * price

        Each daily record also contains the vehicle,
        service, and parts responsible for the income.
        """

        statement = select(ProjectRecord).where(
            ProjectRecord.project_id == project_id
        )

        records = self.db.execute(statement).scalars().all()

        # ---------------------------------------------------------
        # Basic statistics
        # ---------------------------------------------------------

        total_vehicles = len(records)

        service_records = 0

        # ---------------------------------------------------------
        # Daily income totals
        # ---------------------------------------------------------

        daily_income: dict[str, Decimal] = defaultdict(
            lambda: Decimal("0")
        )

        # ---------------------------------------------------------
        # Daily income details
        #
        # Example:
        #
        # {
        #     "2026-09-18": [
        #         {
        #             "plate_number": "ABC 1234",
        #             "vehicle": "Toyota Vios",
        #             "service_id": "...",
        #             "service_performed": "...",
        #             "parts": [...]
        #         }
        #     ]
        # }
        # ---------------------------------------------------------

        daily_income_records: dict[str, list] = defaultdict(list)

        # ---------------------------------------------------------
        # Process vehicle records
        # ---------------------------------------------------------

        for record in records:
            data = record.data or {}

            services = data.get("services", [])

            service_records += len(services)

            # Vehicle information
            plate_number = data.get("plateNumber", "")
            make = data.get("make", "")
            model = data.get("model", "")
            owner_name = data.get("ownerName", "")

            vehicle_name = " ".join(
                value
                for value in [make, model]
                if value
            ).strip()

            # -----------------------------------------------------
            # Process services
            # -----------------------------------------------------

            for service in services:
                service_date = service.get("serviceDate")

                if not service_date:
                    continue

                # Only process selected month.
                if not service_date.startswith(
                    f"{year:04d}-{month:02d}"
                ):
                    continue

                parts = service.get("parts", [])

                # Store only parts that actually generate income.
                service_parts = []

                service_income = Decimal("0")

                # -------------------------------------------------
                # Process parts
                # -------------------------------------------------

                for part in parts:
                    quantity = Decimal(
                        str(part.get("quantity", 0) or 0)
                    )

                    price = Decimal(
                        str(part.get("price", 0) or 0)
                    )

                    income = quantity * price

                    # Add to daily total.
                    daily_income[service_date] += income

                    # Add to service total.
                    service_income += income

                    # Add part detail.
                    service_parts.append(
                        {
                            "id": part.get("id"),
                            "name": part.get("name", ""),
                            "quantity": float(quantity),
                            "price": float(price),
                            "total": float(income),
                        }
                    )

                # -------------------------------------------------
                # Only add a record when there is actual income.
                # -------------------------------------------------

                if service_income > 0:
                    daily_income_records[service_date].append(
                        {
                            "vehicle": vehicle_name,
                            "plate_number": plate_number,
                            "owner_name": owner_name,
                            "service_id": service.get("id"),
                            "service_performed": service.get(
                                "servicePerformed",
                                "",
                            ),
                            "service_income": float(
                                service_income
                            ),
                            "parts": service_parts,
                        }
                    )

        # ---------------------------------------------------------
        # Monthly totals
        # ---------------------------------------------------------

        monthly_income = sum(
            daily_income.values(),
            Decimal("0"),
        )

        # Expenses are not yet stored.
        monthly_expenses = Decimal("0")

        monthly_balance = (
            monthly_income - monthly_expenses
        )

        # ---------------------------------------------------------
        # Determine last day to display
        # ---------------------------------------------------------

        days_in_month = calendar.monthrange(
            year,
            month,
        )[1]

        today = date.today()

        if year == today.year and month == today.month:
            last_day = today.day
        else:
            last_day = days_in_month

        # ---------------------------------------------------------
        # Build daily analytics
        # ---------------------------------------------------------

        daily = []

        # Newest → oldest
        for day in range(last_day, 0, -1):
            date_string = (
                f"{year:04d}-{month:02d}-{day:02d}"
            )

            income = daily_income.get(
                date_string,
                Decimal("0"),
            )

            expenses = Decimal("0")

            balance = income - expenses

            daily.append(
                {
                    "date": date_string,
                    "income": float(income),
                    "expenses": float(expenses),
                    "balance": float(balance),

                    # NEW
                    "income_records": daily_income_records.get(
                        date_string,
                        [],
                    ),
                }
            )

        # ---------------------------------------------------------
        # Return analytics
        # ---------------------------------------------------------

        return {
            "total_vehicles": total_vehicles,
            "service_records": service_records,
            "financial": {
                "month": f"{year:04d}-{month:02d}",
                "income": float(monthly_income),
                "expenses": float(monthly_expenses),
                "balance": float(monthly_balance),
                "daily": daily,
            },
        }