class ForecastEtIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ForecastEtIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        
        field_num = int(slots["field_num"].value)
        days = int(slots["days"].value)
        
        url = "https://rt8uxpcej1.execute-api.eu-central-1.amazonaws.com/dev/forecast-eto"
        
        response = requests.post(url, json={"field_num": field_num, "days": days})
        data = json.loads(response.text)
        
        if days == 1:
            speak_output = "Nel campo " + str(field_num) + ", tra " + str(days) + " giorno è prevista una evotraspirazione di " + str(round(data["body"], 2)) + " millimetri"
        else:
            speak_output = "Nel campo " + str(field_num) + ", tra " + str(days) + " giorni è prevista una evotraspirazione di " + str(round(data["body"], 2)) + " millimetri"
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

sb.add_request_handler(ForecastEtIntentHandler())