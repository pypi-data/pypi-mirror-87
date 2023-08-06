from db import DB

dbh = DB(debug=False)
registree_set = dbh.get_registrees(14)
print(registree_set.events)
print(registree_set.events.cost, registree_set.events.get_costs_per_item())
print(registree_set.payments)
print(registree_set.cost)
print(registree_set.extras)
print(registree_set.extras.cost, registree_set.extras.get_costs_per_item())
for reg in registree_set.registrees:
    print(reg)
print(registree_set.registree_names)
print(registree_set.registree_first_names)
print(registree_set.file_name_names)
print(registree_set.paid, registree_set.paid_in_full, registree_set.still_owed)
print(registree_set.deposit)

# payees = dbh.get_2020_payees()
# for (r, (name, amt)) in payees.items():
#     print(f"{r:003}: {name}: R{amt}")


# registrees = dbh.get_all_registrees()
# for reg in registrees:
#     print(reg.titled_first_names)
