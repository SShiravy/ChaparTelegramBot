from Database import db_methods

# TODO: use db_methods.get_user_deliveries to get all deliveries of a user
# TODO: then in a for loop create the buttons with delivery.name as button text and delivery.id as callback data
# TODO: after clicking one delivery, Show Delivery Control pannel 
# TODO: if user clicked to disabel the delivery simply write: "delivery.active = False" and then call db_methods.update_delivery(delivery); same for enable delivery
# TODO: if user clicked to get summary, display delivery.n_forwarded_msg, delivery.source_id, delivery.destination_id
