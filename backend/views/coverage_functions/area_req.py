from backend.models import Area, Piece, Arearack, Userrack
from django.contrib.auth.models import User

def area_assess(user, location, user_coverage, cam_req_dicts, req_items):
    
    user_rack = user.piece_set.all()
    user_rack = sorted(user_rack, key=lambda user_rack: user_rack.min_size)
    req_items = req_items
    area_rack = location.piece_set.all()
    versatile_leftovers = []
    area_coverage_percent = 0
    for item in area_rack:
        req_items.append(item)
    checked = []
    range_quantities = cam_req_dicts
    unsatisfied = len(req_items) * 7
    compare = len(req_items) * 7
    for req in range_quantities:
        unsatisfied = unsatisfied + (req['upper'] - req['lower']) * req['quantity']
        compare = compare + (req['upper'] - req['lower']) * req['quantity']
        if len(user_coverage) != 0:
            for item in user_coverage:
                item['quantity'] = item['quantity'] + len(versatile_leftovers)
                #account for smaller pieces representing more coverage than 
                if item != []:
                    # if req['offset'] == True:
                    #ADD ^
                    if item['upper'] > req['lower'] or item['lower'] > req['upper']:
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
        for gear in user_rack:
                if gear.gear_type == "Nut" or gear.gear_type == "tricam":
                    min_check = gear.min_size * 0.16
                    min_min = gear.min_size - min_check
                    min_max = gear.min_size + min_check
                    for other_gear in user_rack:
                        if other_gear.min_size < min_max and other_gear.min_size > min_min:
                            checked.append(other_gear)
        for gear in user_rack:
                if gear.gear_type == "Cam" and gear.offset == True:
                    min_check = gear.min_size * 0.16
                    min_min = gear.min_size - min_check
                    min_max = gear.min_size + min_check
                    for other in user_rack:
                        if other.gear_type == "Cam" and other.offset == True:
                            if other.min_size < min_max and other.min_size > min_min:
                                checked.append(other)
        if item == "offset cam":
            for gear in user_rack:
                if gear.gear_type == "Cam" and gear.offset == True:
                    checked.append(gear)
                    unsatisfied = unsatisfied - 7

        if item == "standard":
            for gear in user_rack:
                if gear.gear_type == "Nut" and gear.min_size > 9 and gear not in checked:
                    checked.append(gear)
                    unsatisfied = unsatisfied - 7
        if item == "micro":
            for gear in user_rack:
                if gear.gear_type == "Nut" and gear.min_size < 9 and gear not in checked:
                    checked.append(gear)
                    unsatisfied = unsatisfied - 7
        if item == "standard offset":
            for gear in user_rack:
                if gear.gear_type == "Nut" and gear.min_size > 9 and gear.offset == True and gear not in checked:
                    checked.append(gear)
                    unsatisfied = unsatisfied - 7
        if item == "micro offset":
            for gear in user_rack:
                if gear.gear_type == "Nut" and gear.min_size < 9 and gear.offset == True and gear not in checked:
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
    print("unsat", unsatisfied)
    print(compare)
    area_coverage_percent = ((compare / unsatisfied) * 100)
    if area_coverage_percent > 97:
        area_coverage_percent = 100
    area_coverage_percent = float('%.2f' % area_coverage_percent)
    return area_coverage_percent      

def area_req(user, location, user_coverage):

    s_cam_req = {"upper": 80, "lower": 15, "quantity": 2}
    s_req = [] 
    x = 10
    while x > 0:
        s_req.append("standard")
        x -= 1
    cam_req = []
    cam_req.append(s_cam_req)
    req_items = s_req
    if location.name == "New River Gorge":
        cam_req[0]["lower"] = 10
        req_items.append("micro")
        y = 0
        y = area_assess(user, location, user_coverage, cam_req, req_items)
        return y
    elif location.name == "Yosemite":
        cam_req[0]["lower"] = 10
        cam_req[0]["upper"] = 100
        x = 6
        while x > 0:
            s_req.append("micro")
            s_req.append("micro offset")
            s_req.append("offset cam")
            x -= 1
        y = 0
        y = area_assess(user, location, user_coverage, cam_req, req_items)
        return y
    elif location.name == "Vedauwoo":
        cam_req[0]["upper"] = 190
        req_items.append("Big Bro")
        req_items.append("Big Bro")
        req_items.append("Big Bro")
    else:
        return "not cool"

      
                



