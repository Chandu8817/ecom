
console.log("Sanity check!");

// Get Stripe publishable key
fetch("/config/")
.then((result) => { return result.json(); })
.then((data) => {
  // Initialize Stripe.js
  const stripe = Stripe('pk_test_51ImWnySAF2GIiT99sJFhuKh0FIxgA3ZsmgzuaTr9KQ49eajJfuj5WTyaM0AQFiuuGxoVmK3JkUOJoGD1GW1nYUHl00UBpxOnIN');

  // new
  // Event handler
  document.querySelector("#submitBtn").addEventListener("click", () => {
    // Get Checkout Session ID
    fetch("/create-checkout-session/")
    .then((result) => { return result.json(); })
    .then((data) => {
      console.log(data);
      // Redirect to Stripe Checkout
      return stripe.redirectToCheckout({sessionId: data.sessionId})
    })
    .then((res) => {
      console.log(res);
    });
  });
});