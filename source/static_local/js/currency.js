// handles updating UI with currency changes.
jQuery(document).ready(function ($) {

	var currencyForm = $(".currency-ajax-form")
	var priceElement = $(".ajax-price")
	var detailPriceElement = $(".ajax-detail-price")
	var cartAccountElement = $(".ajax-cart-account-price")
	var cartTotalElement = $(".ajax-cart-total")

	currencyForm.change(function () {
		var thisForm = $(this)
		var actionEndpoint = thisForm.attr("data-endpoint")
		var httpMethod = thisForm.attr("method")
		var formData = thisForm.serialize()

		$.ajax({
			url: actionEndpoint,
			method: httpMethod,
			data: formData,
			success: function(data) {

				var currency = ""
				if (data.currency == "USD"){
					currency = "&dollar;"	
				} else if (data.currency == "GBP"){
					currency = "&pound;"
				} else if (data.currency == "EUR"){
					currency = "&euro;"
				}
				
				priceElement.each(function(i){
	    			$(this).html("<span class='amount'>" + currency +
	    				data.account_prices[i] + "</span>")
				})

				detailPriceElement.html("<span class='amount'>" + currency +
	    				data.detail_account_price + "</span>")


				cartAccountElement.each(function(i){
					$(this).html("<span class='amount'>" + currency +
	    				data.cart_prices[i] + "</span>")
				})

				cartTotalElement.html("<span class='amount'>" + currency +
					data.cart_total + "</span>")

			},
			error: function(error) {
				// error
				console.log("ERROR")
			}
		})
	})
})