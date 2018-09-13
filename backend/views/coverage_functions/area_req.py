from backend.models import Area, Piece, Arearack, Userrack
s_lower = 15
s_upper =  80
s_req = []

def area_req(user, location, user_coverage):
    if location.name == "New River Gorge":
        return nrg(user_coverage)

def nrg(user, location, user_coverage):
    user_rack = user.userrack.pieces.all()
    user_rack = sorted(user_rack, key=lambda user_rack: user_rack.min_size)
    req_items = ["standard", "micro"]
    area_rack = location.piece_set.all()
    for item in area_rack:
        req_items.append(item)
    checked = []
    req_items.append(s_req)
    range_quantities = [{"upper": s_upper, "lower": 10, "quantity": 2, "weight": (self.upper - self.lower) * self.quantity}]
    unsatisfied = len(req_items) * 7
    compare = lend(req_items) * 7
    for req in range_quantities:
        unsatisfied = unsatisfied + req.weight
        compare = compare + req.weight
        versatile_leftovers = 0
        for item in user_coverage:
            if item.upper <= req.lower and item.lower < req.upper:
                item.quantity = item.quantity + versatile_leftovers
                if item.quantity >= req.quantity:
                    satisfied = (item.upper - item.lower) * req.quantity
                    unsatisfied = unsatisfied - satisfied
                
                else:
                    if len(item.versatile) != 0:
                        reqnumber = req.quantity
                        while reqnumber > 0 and len(item.versatile) > 0:
                            for number in item.versatile:
                                unsatisfied = unsatisfied - 7
                                reqnumber = reqnumber - 1
                                item.versatile.remove(number)
                    else:
                        satisfied = (item.upper - item.lower) * item.quantity
                        unsatisfied = unsatisfied - satisfied

                versatile_leftovers = len(item.versatile)
                    #move to the quantity of the next highest size

        
    
    for item in req_items:
        #add offsets later
        if item == "standard":
            for gear in user_rack:
                if item.passive == True and item.active == False and item.min_size > 9 and item not in checked:
                    checked.append(item)
                    unsatisfied = unsatisfied - 7
        if item == "micro":
            for gear in user_rack:
                if item.passive == True and item.active == False and item.min_size < 9 and not in checked:
                    checked.append(item)
                    unsatisfied = unsatisfied - 7
        else:
            for gear in user_rack:
                if item == gear:
                    if gear.quantity > 0:
                        gear.quantity - 1
                        unsatisfied = unsatisfied - 7
    
    area_coverage_percent = 100 - ((unsatisfied / compare) * 100)
    return area_coverage_percent            
                



