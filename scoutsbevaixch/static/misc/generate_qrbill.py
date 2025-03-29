from qrbill import QRBill
my_bill = QRBill(
    account='CH1180808006823590230',
    creditor={
        'name': 'Groupe Scout de l\'Abbaye', 'pcode': '2022', 'city': 'Bevaix', 'street': 'Charcottet 10', 'country': 'CH',
    },
    top_line=False,
    language='fr',
)
my_bill.as_svg('./qrbill.svg')
