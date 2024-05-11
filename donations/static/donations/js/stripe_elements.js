const stripePublicKey = document
  .getElementById("stripe_public_key")
  .textContent.slice(1, -1);
const stripe = Stripe(stripePublicKey);
const elements = stripe.elements();

const style = {
  base: {
    color: "#000",
    fontFamily: '"Roboto", sans-serif',
    fontSmoothing: "antialiased",
    fontSize: "16px",
    "::placeholder": {
      color: "#aab7c4",
    },
  },
  invalid: {
    color: "#dc3545",
    iconColor: "#dc3545",
  },
};

const card = elements.create("card", { style: style });
card.mount("#card-element");

let form = document.getElementById("donation_form");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const donationAmount = document.getElementById("id_amount").value;
  const csrftoken = document.querySelector(
    'input[name="csrfmiddlewaretoken"]'
  ).value;
  const saveInfo = Boolean(document.getElementById("id_save_info").checked);
  const cacheUrl = "/donations/cache_donation_data/";
  const intentUrl = "/donations/create_payment_intent/";

  try {
    const response = await fetch(intentUrl, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken,
      },
      body: JSON.stringify({
        donation_amount: donationAmount,
      }),
    });

    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    const data = await response.json();
    const clientSecret = data.client_secret;

    let postData = {
      csrfmiddlewaretoken: csrftoken,
      client_secret: clientSecret,
      message: form.message.value,
      donation_amount: donationAmount,
    };
    if (saveInfo) {
      postData["save_info"] = saveInfo;
    }

    // Post data to cache_donation_data URL
    const cacheResponse = await fetch(cacheUrl, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken,
      },
      body: JSON.stringify(postData),
    });

    if (!cacheResponse.ok) {
      throw new Error("Error caching donation data");
    }

    const paymentResult = await stripe.confirmCardPayment(clientSecret, {
      payment_method: {
        card: card,
        billing_details: {
          name: form.name.value,
          phone: form.phone.value,
          email: form.email.value,
          address: {
            line1: form.address1.value,
            line2: form.address2.value,
            city: form.city_or_town.value,
            postal_code: form.eircode.value,
            state: form.county.value,
            country: form.country.value,
          },
        },
      },
    });

    if (paymentResult.error) {
      throw new Error(paymentResult.error.message);
    } else {
      const clientSecretInput = document.createElement("input");
      clientSecretInput.type = "hidden";
      clientSecretInput.name = "client_secret";
      clientSecretInput.value = clientSecret;
      form.appendChild(clientSecretInput);
      form.submit();
    }
  } catch (error) {
    console.error("Error processing payment:", error);
    alert("Error processing payment. Please try again.");
  }
});
