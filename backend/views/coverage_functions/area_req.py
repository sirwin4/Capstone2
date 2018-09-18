from backend.models import Area, Piece, Arearack, Userrack
s_lower = 15
s_upper =  80
s_req = []

def nrg(user, location, user_coverage):
    user_rack = user.piece_set.all()
    user_rack = sorted(user_rack, key=lambda user_rack: user_rack.min_size)
    req_items = ["standard", "micro"]
    area_rack = location.piece_set.all()
    versatile_leftovers = []
    for item in area_rack:
        req_items.append(item)
    checked = []
    req_items.append(s_req)
    range_quantities = [{"upper": s_upper, "lower": 10, "quantity": 2}]
    unsatisfied = len(req_items) * 7
    compare = len(req_items) * 7
    for req in range_quantities:
        unsatisfied = unsatisfied + (req['upper'] - req['lower']) * req['quantity']
        compare = compare + (req['upper'] - req['lower']) * req['quantity']
        for item in user_coverage:
            item['quantity'] = item['quantity'] + len(versatile_leftovers)
            print("all items", item)
            #account for smaller pieces representing more coverage than 
            if item != []:
                if item['upper'] < req['lower'] or item['lower'] < req['upper']:
                    if item['quantity'] >= req['quantity']:
                        if item['lower'] >= req['lower'] and item['upper'] <= req['upper']:
                            satisfied = (item['upper'] - item['lower']) * req['quantity']
                            unsatisfied = unsatisfied - satisfied
                        elif item['upper'] > req['upper']:
                            satisfied = (req['upper'] - item['lower']) * req['quantity']
                            unsatisfied = unsatisfied - satisfied
                        elif item['lower'] < req['lower']:
                            satisfied = (item['upper'] - req['lower']) * req['quantity']
                            unsatisfied = unsatisfied - satisfied
                    
                    else:
                        if len(item['versatile']) != 0:
                            reqnumber = req['quantity']
                            while reqnumber > 0 and len(item['versatile']) > 0:
                                for number in item['versatile']:
                                    if number['upper'] <= req['lower'] and number['lower'] < req['upper']:
                                        satisfied = (number['upper'] - number['lower']) * number['quantity']
                                        unsatisfied = unsatisfied - satisfied
                                        item['versatile'].remove(number)
                                    elif number['upper'] > req['upper']:
                                        satisfied = (req['upper'] - number['lower']) * number['quantity']
                                        unsatisfied = unsatisfied - satisfied
                                        item['versatile'].remove(number)
                                    elif number['lower'] < req['lower']:
                                        satisfied = (number['upper'] - req['lower']) * number['quantity']
                                        unsatisfied = unsatisfied - satisfied
                                        item['versatile'].remove(number)
                        else:
                            if item['lower'] < 20:
                                unsatisfied = unsatisfied + (10 * (req['quantity'] - item['quantity']))
                            elif item ['lower'] < 40:
                                unsatisfied = unsatisfied + (5 * (req['quantity'] - item['quantity']))
                            if item['lower'] >= req['lower'] and item['upper'] < req['upper']:
                                satisfied = (item['upper'] - item['lower']) * item['quantity']
                                unsatisfied = unsatisfied - satisfied
                            elif item['upper'] > req['upper']:
                                satisfied = (req['upper'] - item['lower']) * item['quantity']
                                unsatisfied = unsatisfied - satisfied
                            elif item['lower'] < req['lower']:
                                satisfied = (item['upper'] - req['lower']) * item['quantity']
                                unsatisfied = unsatisfied - satisfied
                                
                    versatile_leftovers = item['versatile']
                        #move to the quantity of the next highest size

        
    
    for item in req_items:
        #add offsets later
        if item == "standard":
            for gear in user_rack:
                if gear.SLCD== False and gear.min_size > 9 and gear not in checked:
                    checked.append(gear)
                    unsatisfied = unsatisfied - 7
        if item == "micro":
            for gear in user_rack:
                if gear.SLCD == False and gear.min_size < 9 and gear not in checked:
                    checked.append(gear)
                    unsatisfied = unsatisfied - 7
        else:
            
            cover = Userrack.objects.filter(user=user)
            coverage_list = []
            for item in cover:
                numbered_piece = item.piece
                setattr(numbered_piece, 'quantity', item.quantity)
                coverage_list.append(numbered_piece)
            for gear in coverage_list:
                if item == gear:
                    if gear.quantity > 0:
                        gear.quantity - 1
                        unsatisfied = unsatisfied - 7
    print('unsatisfied', unsatisfied)
    print(compare)
    area_coverage_percent = 100 - ((unsatisfied / compare) * 100)
    if area_coverage_percent > 97:
        area_coverage_percent = 100
    return area_coverage_percent      

def area_req(user, location, user_coverage):
    if location.name == "New River Gorge":
        return nrg(user, location, user_coverage)

      
                



