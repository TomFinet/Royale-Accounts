from .forms import CurrencyForm

def currency_context(request):
	return {"currency": request.session.get("currency", "USD")}

def currency_form_context(request):
	currency = request.session.get("currency", "USD")
	form = CurrencyForm(initial={'currency': currency})
	return {"currency_form": form}

