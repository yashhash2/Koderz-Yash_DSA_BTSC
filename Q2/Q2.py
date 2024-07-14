class Seat:
    def __init__(self, seat_id, seat_type):
        self.seat_id = seat_id
        self.seat_type = seat_type
        self.reserved = False
    
    def reserve(self):
        if not self.reserved:
            self.reserved = True
            return True
        return False
    
    def cancel_reservation(self):
        if self.reserved:
            self.reserved = False
            return True
        return False


class Row:
    def __init__(self, row_id, seat_types):
        self.row_id = row_id
        self.seats = [Seat(f"{row_id}{seat_type}", seat_type) for seat_type in seat_types]
    
    def get_seat(self, seat_type):
        for seat in self.seats:
            if seat.seat_type == seat_type and not seat.reserved:
                return seat
        return None
    
    def get_any_available_seat(self):
        for seat in self.seats:
            if not seat.reserved:
                return seat
        return None


class Flight:
    def __init__(self, flight_id, seat_layout):
        self.flight_id = flight_id
        self.rows = [Row(row_id, seat_layout) for row_id in range(1, len(seat_layout) + 1)]
        self.waiting_list = []
        self.max_waiting_list_size = len(seat_layout) * 5 // 100
    
    def initialize_flight(self, seat_layout):
        self.rows = [Row(row_id, seat_layout) for row_id in range(1, len(seat_layout) + 1)]
    
    def reserve_seat(self, preference):
        for row in self.rows:
            if preference == 'any':
                seat = row.get_any_available_seat()
            else:
                seat = row.get_seat(preference[0].upper())
            
            if seat and seat.reserve():
                return seat.seat_id
        return self.add_to_waiting_list(preference)
    
    def check_seat_availability(self, preference):
        for row in self.rows:
            seat = row.get_seat(preference[0].upper())
            if seat and not seat.reserved:
                return True
        return False
    
    def suggest_optimal_seat(self, preference):
        for row in self.rows:
            if preference == 'any':
                seat = row.get_any_available_seat()
            else:
                seat = row.get_seat(preference[0].upper())
            
            if seat and not seat.reserved:
                return seat.seat_id
        return None
    
    def add_to_waiting_list(self, preference):
        if len(self.waiting_list) < self.max_waiting_list_size:
            self.waiting_list.append(preference)
            return "Added to waiting list"
        return "Flight and waiting list full"
    
    def cancel_reservation(self, seat_id):
        for row in self.rows:
            for seat in row.seats:
                if seat.seat_id == seat_id:
                    if seat.cancel_reservation():
                        if self.waiting_list:
                            preference = self.waiting_list.pop(0)
                            self.reserve_seat(preference)
                        return True
        return False
    
    def change_reservation(self, old_seat_id, new_preference):
        if self.cancel_reservation(old_seat_id):
            return self.reserve_seat(new_preference)
        return None


class SkyWings:
    def __init__(self):
        self.flights = {}
    
    def add_flight(self, flight_id, seat_layout):
        self.flights[flight_id] = Flight(flight_id, seat_layout)
    
    def initialize_flight(self, flight_id, seat_layout):
        if flight_id in self.flights:
            self.flights[flight_id].initialize_flight(seat_layout)
        else:
            self.add_flight(flight_id, seat_layout)
    
    def reserve_seat(self, flight_id, preference):
        if flight_id in self.flights:
            return self.flights[flight_id].reserve_seat(preference)
        return None
    
    def check_seat_availability(self, flight_id, preference):
        if flight_id in self.flights:
            return self.flights[flight_id].check_seat_availability(preference)
        return False
    
    def suggest_optimal_seat(self, flight_id, preference):
        if flight_id in self.flights:
            return self.flights[flight_id].suggest_optimal_seat(preference)
        return None
    
    def cancel_reservation(self, flight_id, seat_id):
        if flight_id in self.flights:
            return self.flights[flight_id].cancel_reservation(seat_id)
        return False
    
    def change_reservation(self, flight_id, old_seat_id, new_preference):
        if flight_id in self.flights:
            return self.flights[flight_id].change_reservation(old_seat_id, new_preference)
        return None


# Initialize SkyWings system
skywings = SkyWings()

# Sample seat layout for a flight
seat_layout = ['W', 'M', 'A', 'M', 'W']

# Add a flight
skywings.add_flight("SK123", seat_layout)

# Reserve a window seat
print(skywings.reserve_seat("SK123", "window"))

# Check seat availability for an aisle seat
print(skywings.check_seat_availability("SK123", "aisle"))

# Suggest an optimal seat for an aisle preference
print(skywings.suggest_optimal_seat("SK123", "aisle"))

# Cancel a reservation
print(skywings.cancel_reservation("SK123", "1W"))

# Change a reservation
print(skywings.change_reservation("SK123", "1M", "window"))
