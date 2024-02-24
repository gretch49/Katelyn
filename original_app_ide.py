import os
import openai

### REPLACE WITH YOU API KEY
my_api_key = "YOUR-API-KEY"
client = openai.OpenAI(api_key=my_api_key)

def generate_itinerary(prompt):

    response = client.chat.completions.create(model="gpt-4",
    messages=[
        {"role": "system", "content": f"You are a virtual travel assistant named Katelyn. Your task is to create a travel itinerary based on these parameters: {prompt} Keep the itinerary to less than 2000 characters. Give the user a basic link to the country or city's homepage for more resources."},  # Correctly formatted system message
        {"role": "user", "content": "Please generate the itinerary."}  # User message prompting the action
    ],
    max_tokens=2000)
    
    # Correctly extract and return the generated itinerary from the API response
    return response.choices[0].message.content.strip()

def generate_route(route_prompt): 
    response = client.chat.completions.create(model="gpt-4",
    messages=[
        {"role": "system", "content": f"How prepared does this sentence sound on a scale of 1 to 10? 1 is not very prepared. 5 is a little prepared. 10 is very prepared. Return a number only. The sentence is: {route_prompt}"},  # Correctly formatted system message
        {"role": "user", "content": "Please generate the route."}  # User message prompting the action
    ],
    max_tokens=1)
    
    # Correctly extract and return the generated itinerary from the API response
    return response.choices[0].message.content.strip()


def main():
    print("\n\nHi, I'm Katelyn, your virtual travel assistant.  I’m excited to help you plan your trip! \n")
    q_loc = 'First, where are you going? You can be specific, like “New York City,” or more general, like “Eastern Europe.” '
    q_when = 'I’ve always wanted to go there! When do you plan on going? If you’re not sure, you can say “unsure.” '
    q_travelers = 'Who do you plan on going with? I’d like to know their ages and names, or their relationships to you.' \
            ' If it’s a solo trip, you can say “myself.” '
    q_act = 'Now for the fun stuff! What do you (and your companions) like to do on vacation? Maybe you’re a big ' \
        '“lounge on the beach and suntan” kind of travelers, but I bet you want to do some activities too! Tell me ' \
            'some activities you enjoy, like biking, sight-seeing, eating local cuisine, shopping, or meeting new people. '
    q_bud = 'Finally, let’s talk logistics. What’s your estimated budget for this trip? I’ll assume USD unless you specify otherwise. '
    q_loc_unsure = 'First, where are you going? You can be specific, like “New York City,” or more general, like “Eastern Europe.”' \
    'If you’re not sure, you can say “unsure.” '
    q_wea = 'I understand, it’s a big world out there! Let me help you narrow down some ideas. Do you prefer warm weather or ' \
    'cool weather? '
    q_dur_b = 'How long do you plan to travel for? You can say something general like “a few days,” or be more specific and say ' \
    'something like “2 weeks.” If you’re not sure, you can say “unsure.” '
    q_res_b = 'Do you have any restrictions on going out of the US? '
    q_loc_c = 'Is there anywhere you’d like to go to? You can be specific, like “New York City,” or more general, like “Eastern Europe.” ' \
    ' If you’re not sure, you can say “unsure.” '
    q_wea_c = 'Here’s the first question. Do you prefer warm weather or cool weather? '
    q_when_bc = 'When do you plan on going? If you’re not sure, you can say “unsure.” '
    q_other = 'Do you have any other considerations for me to keep in mind? For example, you could tell me you don’t want to go hiking, or that you’re traveling with someone with specific needs. Otherwise, you can just say "no." '
    q_reccos = 'Let me know if there are things you specifically want recommendations on, like where to rent a car, what the best budget hotel is, or how to use public transit. '
    q_transpo = "And have you thought about how you'll be getting around? Let me know if you plan on using your own car, renting a car, using public transit, or a mixture of transportation. "
    q_home = "So I can better plan for your budget, where are you traveling from? In other words, where's home for you? "

    route_prompt = input("To get started, I’d like to know how much of your trip you have planned. \n \nHave you planned a lot already, or is the world your oyster? \n \n")
    route_response = int(generate_route(route_prompt))
    
    if route_response >= 7:
        print("\nOkay, great! You have a good idea of where and when your trip will be. Maybe you already have your plane tickets or your car is gassed up and ready to go. Let me ask you some questions to better plan an itinerary for you. ")
        location = input(q_loc)
        when = input(q_when)
        duration = input(f'Okay. How long do you plan to be in {location}? You can say something general like “a few days,” ' \
        ' or be more specific and say something like “2 weeks.” If you’re not sure, you can say “unsure.” ')
        travelers = input(q_travelers)
        activities = input(q_act)            
        budget = str(input(q_bud))
        transportation = input(q_transpo)
        other = input(q_other)
        recommendations = input(q_reccos)
        home = input(q_home)

    elif route_response >= 4:
        print("\nIt sounds like you’ve got some ideas, but you might want some guidance. I can help with that! \n")
        location = input(q_loc_unsure)
        if "unsure" in location.lower():
            weather = input(q_wea)                
            when = input(q_when_bc)
            restrictions = input(q_res_b)
            duration = input(q_dur_b)
            travelers = input(q_travelers)
            activities = input(q_act)
            budget = str(input(q_bud))
            transportation = input(q_transpo)
            other = input(q_other)
            recommendations = input(q_reccos)
            home = input(q_home)         
        else: 
            when = input(q_when)
            duration = input(f'Okay. How long do you plan to be in {location}? ')
            travelers = input(q_travelers)
            activities = input(q_act)
            budget = str(input(q_bud))
            transportation = input(q_transpo)
            other = input(q_other)            
            recommendations = input(q_reccos)
            home = input(q_home)
    else:
        print("\nCool, I’d love to help you plan this trip! Let me ask you some questions about yourself to get started.\n\n")
        location = "Looking for suggestions based on weather, season, budget, and activities."
        weather = input(q_wea_c)
        when = input(q_when_bc)
        restrictions = input(q_res_b)
        duration = input(q_dur_b)
        travelers = input(q_travelers)
        activities = input(q_act)
        budget = str(input(q_bud))
        other = input(q_other)
        transportation = input(q_transpo)
        recommendations = input(q_reccos)
        home = input(q_home)
       

    prompt = f' Location: {location} \n When: {when} \n Duration: {duration} \n Travelers: {travelers} and I \n Preferred activities: {activities} \n Budget (in USD unless otherwise specified): {budget} \n Transportation: {transportation} \n Other considerations: {other} {route_prompt} \n Specific recommendations: {recommendations} \n Origin location: {home}'
    print("\n Great. Give me a moment while I research an itinerary for you.")
    itinerary = generate_itinerary(prompt)
    print("\nHere's what I came up with!\n")        
    print("*"*20)
    print(itinerary)
    print("*"*20)




if __name__ == "__main__":
    main()
