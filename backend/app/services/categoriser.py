"""Transaction categorization service."""
import structlog
from typing import List

logger = structlog.get_logger(__name__)

# Category keywords mapping
CATEGORY_KEYWORDS = {
    "salary": [
        "salary",
        "payroll",
        "wage",
        "payment",
        "credit",
        "deposit",
        "transfer in",
    ],
    "emi": [
        "emi",
        "loan",
        "mortgage",
        "credit card",
        "monthly installment",
        "car loan",
        "home loan",
        "personal loan",
    ],
    "food": [
        "restaurant",
        "cafe",
        "food",
        "swiggy",
        "zomato",
        "delivery",
        "dominos",
        "pizza",
        "burger",
        "kfc",
        "mcdonalds",
    ],
    "transport": [
        "fuel",
        "petrol",
        "diesel",
        "pump",
        "uber",
        "ola",
        "taxi",
        "auto",
        "parking",
        "bus",
        "train",
        "flight",
    ],
    "shopping": [
        "amazon",
        "flipkart",
        "myntra",
        "ajio",
        "ebay",
        "shopping",
        "store",
        "mall",
        "retail",
        "clothes",
        "apparels",
        "fashion",
    ],
    "utilities": [
        "electricity",
        "water",
        "gas",
        "bill",
        "internet",
        "broadband",
        "airtel",
        "jio",
        "vodafone",
        "recharge",
        "mobile",
        "phone",
    ],
    "entertainment": [
        "netflix",
        "youtube",
        "spotify",
        "cinema",
        "movie",
        "ticket",
        "game",
        "gaming",
        "subscription",
        "prime",
    ],
    "healthcare": [
        "hospital",
        "doctor",
        "medicine",
        "pharmacy",
        "health",
        "medical",
        "insurance",
        "clinic",
        "dental",
    ],
    "education": [
        "school",
        "college",
        "university",
        "course",
        "education",
        "training",
        "udemy",
        "fee",
        "tuition",
    ],
    "insurance": [
        "insurance",
        "policy",
        "premium",
        "aditya",
        "bajaj",
        "hdfc",
    ],
    "transfer": [
        "transfer",
        "neft",
        "rtgs",
        "upi",
        "payment",
        "send",
        "receive",
    ],
}


class TransactionCategorizer:
    """Categorize transactions based on description."""

    @staticmethod
    def categorize(description: str) -> str:
        """Categorize a transaction based on its description."""
        description_lower = description.lower()

        # Check each category
        for category, keywords in CATEGORY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in description_lower:
                    logger.debug("transaction_categorized", category=category, keyword=keyword)
                    return category

        # Default to 'other' if no match
        logger.debug("transaction_not_categorized", description=description[:50])
        return "other"

    @staticmethod
    def is_salary(description: str) -> bool:
        """Check if transaction is salary/income."""
        description_lower = description.lower()
        salary_keywords = CATEGORY_KEYWORDS.get("salary", [])
        return any(keyword in description_lower for keyword in salary_keywords)

    @staticmethod
    def is_emi(description: str) -> bool:
        """Check if transaction is EMI/loan payment."""
        description_lower = description.lower()
        emi_keywords = CATEGORY_KEYWORDS.get("emi", [])
        return any(keyword in description_lower for keyword in emi_keywords)


def categorize_transactions(transactions: List[dict]) -> List[dict]:
    """Categorize a list of transactions."""
    categorizer = TransactionCategorizer()

    for tx in transactions:
        category = categorizer.categorize(tx.get("description", ""))
        tx["category"] = category
        tx["is_salary"] = categorizer.is_salary(tx.get("description", ""))
        tx["is_emi"] = categorizer.is_emi(tx.get("description", ""))

    return transactions
