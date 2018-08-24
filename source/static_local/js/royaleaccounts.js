jQuery(document).ready(function ($) {

	var accountForm = $(".form-account-ajax")

	accountForm.submit(function(event) {
		event.preventDefault()

		var thisForm = $(this)
		var actionEndpoint = thisForm.attr("data-endpoint")
		var httpMethod = thisForm.attr("method")
		var formData = thisForm.serialize()

		$.ajax({
			url: actionEndpoint,
			method: httpMethod,
			data: formData,
			success: function(data) {
				var submitSpan = thisForm.find(".submit-span")
				if (data.added) {
					submitSpan.html("In cart <button type='submit' class='btn btn-link'>Remove?</button>")
					thisForm.find(".add-to-cart-button").html("In Cart, Remove?")
				} else {
					submitSpan.html("<div class='action'><button class='btn btn-primary btn-sm btn-green uppercase cart-button' type='submit'>add to cart</button></div>")
					thisForm.find(".add-to-cart-button").html("Add to Cart")
				}
				
				var navbarCount = $(".navbar-cart-count")
				if (data.cartItemCount == 0) {
					navbarCount.text()
				}
				navbarCount.text(data.cartItemCount)

				var currentPath = window.location.href
				if (currentPath.indexOf("cart") != -1) {
					refreshCart()
				}
			},
			error: function(error) {
				// error
				print("Error")
			}
		})
	})

	function refreshCart() {
		var cartTable = $(".shop_table")
		var cartBody = cartTable.find(".cart-body")
		var accountRows = cartBody.find(".cart_table_item")
		var cartTotalsTable = $(".cart-totals")

		var refreshCartUrl = '/cart/api'
		var refreshCartMethod = "GET"

		$.ajax({
			url: refreshCartUrl,
			method: refreshCartMethod,
			data: {},
			success: function(data) {
				console.log(data)
				var hiddenCartItemRemoveForm = $(".cart-item-remove-form")
				if (data.accounts.length > 0) {
					accountRows.html(" ")

					var currency = ""
					if (data.currency == "USD"){
						currency = "&dollar;"	
					} else if (data.currency == "GBP"){
						currency = "&pound;"
					} else if (data.currency == "EUR"){
						currency = "&euro;"
					}

					$.each(data.accounts, function(index, value){
						var cartItemRemove = hiddenCartItemRemoveForm.clone()
						cartItemRemove.css("display", "block")
						cartItemRemove.find(".cart-item-account-id").val(value.id)

						// check if image is existent
						// use title property in here

						var image = value.img_sml_url
						if (image == null){
							image = "http://placehold.it/100x100"
						}

						cartBody.prepend("<tr><td class='product-thumbnail'><a href='" + value.url + "'>" + 
							"<img width='100' height='100' alt='img' src=" + image + ">" +
							"</a></td>" + "<td class='product-name'><a href='" + value.url + "'>" + value.title + "</a>" +
							"</td><td class='product-price ajax-cart-account-price'><span class='amount'>" + currency +
							value.price + "</span>" + "</td><td class='product-remove'>" + cartItemRemove.html() + "</td></tr>")
					})

					cartTotalsTable.find(".ajax-cart-total")
						.html("<span class='amount'>" + currency + data.total + "</span>")

				} else {
					// empty cart so handle that
					// for the moment just reload the page
					window.location.reload()
				}
			},
			error: function(error) {

			}
		})
	}
});