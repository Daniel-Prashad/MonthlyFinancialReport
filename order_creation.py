import pandas as pd
import datetime
from random import choice, randint, uniform
from faker import Faker

# set the number of orders to be generated
num_orders = 10000



'''CREATION OF THE CUSTOMERS TABLE'''
# define the number of customers and initialize the lists to be used as columns of the Customers table
num_customers = 500
customer_names, customer_type = ([] for i in range(2))

# for each customer, generate the customer name and type of customer
for i in range(1, num_customers + 1):
    customer_names.append('Customer ' + str(i))
    # implement a 70/30 split of regular customer to brokers
    customer_type.append('Regular') if (randint(1,10) <= 7) else customer_type.append('Broker')

# create the Customers table using the generated data
customer_info = {'Customer Account': customer_names, 'Customer Type': customer_type}
customers_df = pd.DataFrame(customer_info)



'''CREATION OF THE PARTNERS TABLE'''
# initialize the data for the Partners table, the name of the carrier, the province that they service and the agreed delivery rate
partner_terminals = [
                    {'Partner Terminal': 'PT British Columbia 1', 'Province Serviced': 'British Columbia', 'Partner Shipping Multiplier': 1.10},
                    {'Partner Terminal': 'PT British Columbia 2', 'Province Serviced': 'British Columbia', 'Partner Shipping Multiplier': 1.08},
                    {'Partner Terminal': 'PT Alberta 1', 'Province Serviced': 'Alberta', 'Partner Shipping Multiplier': 1.08},
                    {'Partner Terminal': 'PT Alberta 2', 'Province Serviced': 'Alberta', 'Partner Shipping Multiplier': 1.07},
                    {'Partner Terminal': 'PT Saskatchewan', 'Province Serviced': 'Saskatchewan', 'Partner Shipping Multiplier': 1.06},
                    {'Partner Terminal': 'PT Manitoba', 'Province Serviced': 'Manitoba', 'Partner Shipping Multiplier': 1.05},
                    {'Partner Terminal': 'PT New Brunswick', 'Province Serviced': 'New Brunswick', 'Partner Shipping Multiplier': 1.05},
                    {'Partner Terminal': 'PT Prince Edward Island', 'Province Serviced': 'Prince Edward Island', 'Partner Shipping Multiplier': 1.06},
                    {'Partner Terminal': 'PT Newfoundland', 'Province Serviced': 'Newfoundland', 'Partner Shipping Multiplier': 1.07}
]

# create the Partners table using the generated data
partners_df = pd.DataFrame(partner_terminals)



'''CREATION OF THE SHIPPERS TABLE'''
# define the number of shipping locations as 40% of the number of total orders
num_shipping_locations = int(num_orders * 0.4)

# intialize a faker generator and a list to store shipping addresses
fake = Faker()
shipping_addresses =[]

# for each shipping location, generate a fake street address
for i in range(0, num_shipping_locations):
    shipping_addresses.append(fake.address().partition('\n')[0])

shippers_df = pd.DataFrame(shipping_addresses, columns=['Shipping Address'])
shippers_df['Shipping Province'] = 'Ontario'



'''CREATION OF THE RECEIVERS TABLE'''
# define the number of RECEIVING locations as 80% of the number of total orders
num_receiving_locations = int(num_orders * 0.8)

# define the dictionary of provinces for final delivery (excluding Ontario) and map a shipping multiplier range to each
provinces = {'British Columbia': [1.20, 1.25], 'Alberta': [1.16, 1.21], 'Saskatchewan': [1.12, 1.15], 'Manitoba': [1.10, 1.15], 'New Brunswick': [1.10, 1.15], 'Prince Edward Island': [1.12, 1.17], 'Newfoundland': [1.17, 1.21]}

# intialize a faker generator and the lists to store receiving addresses and associated provinces and shipping multipliers
fake = Faker()
receiving_addressses, receiving_provinces, shipping_multipliers = ([] for i in range(3))

# for each receiving location, generate a fake street address
for i in range(0, num_shipping_locations):
    receiving_addressses.append(fake.address().partition('\n')[0])
    # implement a 30% chance where the final delivery will be to an address in Ontario
    if (randint(1,10) <= 3):
        receiving_provinces.append('Ontario')
        shipping_multipliers.append(round(uniform(1.07, 1.13),4))
    # otherwise, randomly choose a province from the list of serviced provinces and randomly generate a shipping multiplier to the generated address that falls within the respective range of the respective province
    else:
        selected_province_info = choice(list(provinces.items()))
        receiving_provinces.append(selected_province_info[0])
        shipping_multipliers.append(round(uniform(selected_province_info[1][0], selected_province_info[1][1]),4))

# create the Receivers table using the generated data
receivers_info = {'Receiving Address': receiving_addressses, 'Receiving Province': receiving_provinces, 'Shipping Multiplier': shipping_multipliers}
receivers_df = pd.DataFrame(receivers_info)



'''CREATION OF THE ORDERS TABLE'''
# define a start date, end date and calculate the number of days between the two (all order dates will be between these start and end dates)
start_date = datetime.date(2024, 10, 1)
end_date = datetime.date(2024, 10, 31)
num_days = (end_date - start_date).days

# initialize the lists that will hold the data for each column of the Orders table
order_ids, order_dates, customer_accounts, customer_types, shippers_addresses, shippers_provinces, receivers_addresses, receivers_provinces, order_shipping_multipiers, partner_terminal_names, num_skids, total_weights, shipping_costs, partner_shipping_fees = ([] for i in range(14))

# define the last index for each of the Customers, Shippers and Receivers tables
last_customers_df_index = customers_df.shape[0] - 1
last_shippers_df_index = shippers_df.shape[0] - 1
last_receivers_df_index = receivers_df.shape[0] - 1

# each record in the Orders table is populated as defined below
for i in range(0, num_orders):
    # an order id is assigned
    order_ids.append(1000000 + i)

    # a random date between the start and end dates is selected
    random_day = randint(1, num_days)
    random_date = start_date + datetime.timedelta(days=random_day)
    order_dates.append(random_date)
    
    # a random customer from the Customers table is selected and their data is added to the current record of the Orders table
    random_customer = randint(0, last_customers_df_index)
    customer_accounts.append(customers_df.iloc[random_customer]['Customer Account'])
    customer_types.append(customers_df.iloc[random_customer]['Customer Type'])

    # a random shipper is from the Shippers table is selected and their data is added to the current record of the Orders table
    random_shipper = randint(0, last_shippers_df_index)
    shippers_addresses.append(shippers_df.iloc[random_shipper]['Shipping Address'])
    shippers_provinces.append(shippers_df.iloc[random_shipper]['Shipping Province'])

    # a random receiver is from the Receivers table is selected and their data is added to the current record of the Orders table
    random_receiver = randint(0, last_receivers_df_index)
    receivers_addresses.append(receivers_df.iloc[random_receiver]['Receiving Address'])
    receivers_province = receivers_df.iloc[random_receiver]['Receiving Province']
    receivers_provinces.append(receivers_province)
    shipping_multiplier = receivers_df.iloc[random_receiver]['Shipping Multiplier']
    order_shipping_multipiers.append(shipping_multiplier)

    # using the receiver's province, select the corresponding partnering terminal and their shipping multiplier
    if receivers_province == 'Ontario':
        partner_terminal_names.append('PT Ontario')
        partner_shipping_multiplier = 1.03
    # if the final delivery is destined for an address in either British Columbia or Alberta, then randomly select one of the two available partners in each province
    elif receivers_province == 'British Columbia':
        if randint(1,2) == 1:
            partner_terminal = 'PT British Columbia 1'
        else:
            partner_terminal = 'PT British Columbia 2'
        partner_terminal_names.append(partner_terminal)
        index = partners_df.isin([partner_terminal]).any(axis=1).idxmax()
        partner_shipping_multiplier = partners_df.iloc[index]['Partner Shipping Multiplier']
    elif receivers_province == 'Alberta':
        if randint(1,2) == 1:
            partner_terminal = 'PT Alberta 1'
        else:
            partner_terminal = 'PT Alberta 2'
        partner_terminal_names.append(partner_terminal)
        index = partners_df.isin([partner_terminal]).any(axis=1).idxmax()
        partner_shipping_multiplier = partners_df.iloc[index]['Partner Shipping Multiplier']
    # otherwise, select the partnering terminal and their corresponding shipping multiplier
    else:
        index = partners_df.isin([receivers_province]).any(axis=1).idxmax()
        partner_terminal_names.append(partners_df.iloc[index]['Partner Terminal'])
        partner_shipping_multiplier = partners_df.iloc[index]['Partner Shipping Multiplier']

    # randomly generate the number of skids for this order, between 1 and 8
    num_pcs = randint(1, 26)
    total_weight = 0
    # for each skid, randomly generate a weight between 100lbs and 750lbs and calculate the total weight of the shipment
    for i in range(0, num_pcs):
        weight = randint(100, 750)
        total_weight += weight
    # calculate and store the shipping cost as 15% of the total weight times the shipping multiplier associated with the destined province
    shipping_cost = round(0.15 * total_weight * shipping_multiplier, 2) 

    # add the calculated data to the Orders table
    num_skids.append(num_pcs)
    total_weights.append(total_weight)
    shipping_costs.append(shipping_cost)

    # calculate the shipping fee that will be charged by the partnering terminal and add it to the Orders table
    random_multiplier = round(uniform(0.05, 0.10), 3)
    partner_shipping_fee = round(random_multiplier * total_weight * partner_shipping_multiplier)
    partner_shipping_fees.append(partner_shipping_fee)

# create the Orders table using the generated data
orders_info = {'Order ID': order_ids, 'Order Date': order_dates, 'Customer Account': customer_accounts, 'Customer Type': customer_types, 'Shipping Address': shippers_addresses, 'Shipping Province': shippers_provinces, 'Receiving Address': receivers_addresses,
                'Receiving Province': receivers_provinces, 'Carrier': partner_terminal_names, 'Number of Skids': num_skids, 'Total Weight': total_weights, 'Shipping Cost': shipping_costs, 'Carrier Fee': partner_shipping_fees}
orders_df = pd.DataFrame(orders_info)

# write the Orders table to an excel file
orders_df.to_excel('orders_raw_data_generation.xlsx', index=False, sheet_name='Raw Data')

print("DONE!")