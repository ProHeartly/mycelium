

document.addEventListener('DOMContentLoaded', () => {
    const setupElement = document.getElementById('setup');
    const deliveryElement = document.getElementById('delivery');

    async function getCodingJoke() {
        if (!navigator.onLine) {
            setupElement.textContent = "You appear to be offline.";
            deliveryElement.textContent = "Maybe you like localhost more :p";
        }

        try {
            const response = await fetch('https://v2.jokeapi.dev/joke/Programming?blacklistFlags=nsfw,religious,political,racist,sexist,explicit');

            if (!response.ok) throw new Error("API request failed");

            const data = await response.json();

            if (data.type == 'single') {
                setupElement.textContent = data.joke;
                deliveryElement.textContent = "";
            } else if (data.type == 'twopart') {
                setupElement.textContent = data.setup;
                deliveryElement.textContent = data.delivery;
            }
        } catch (error) {
            setupElement.textContent = "Error 404: Joke module failed to compile.";
            deliveryElement.textContent = "Try reloading the server thread (fix for everything, just reload)"
        }
    }

    getCodingJoke();
});