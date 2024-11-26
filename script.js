const chatHistory = document.getElementById("chat-history");
const searchInput = document.getElementById("search-input");
const searchButton = document.getElementById("search-button");
const newConversationButton = document.getElementById("new-conversation-button");
const menuToggle = document.getElementById("menu-toggle");
const sidebar = document.getElementById("sidebar");
const brandHeaders = document.querySelectorAll(".brand-header");

let currentConversation = [];
let conversationsByBrand = {
    Cumlaude: [],
    Rilastil: [],
    Sensilis: []
};
let activeBrand = null;

// Función para mostrar el mensaje de bienvenida con opciones de marca
function showWelcomeMessage() {
    chatHistory.innerHTML = ""; // Limpiar historial
    const welcomeMessage = document.createElement("div");
    welcomeMessage.classList.add("message", "bot");
    welcomeMessage.innerHTML = `
        Bienvenido, selecciona una marca para comenzar:
        <span class="brand-option" data-brand="Cumlaude">Cumlaude</span>
        <span class="brand-option" data-brand="Rilastil">Rilastil</span>
        <span class="brand-option" data-brand="Sensilis">Sensilis</span>
    `;
    chatHistory.appendChild(welcomeMessage);

    // Añadir eventos a las opciones de marca
    document.querySelectorAll(".brand-option").forEach(option => {
        option.addEventListener("click", (event) => {
            changeActiveBrand(event.target.dataset.brand);
        });
    });
}

// Función para añadir un mensaje al historial del chat
function addMessageToChat(sender, message) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", sender);
    messageDiv.textContent = message;
    chatHistory.appendChild(messageDiv);
    chatHistory.scrollTop = chatHistory.scrollHeight;
    currentConversation.push({ sender, message });
}

// Función para enviar un mensaje
async function sendMessage() {
    const userMessage = searchInput.value.trim();

    if (!userMessage) {
        alert("Por favor, escribe un mensaje antes de enviarlo.");
        return;
    }

    if (!activeBrand) {
        alert("Por favor, selecciona una marca antes de comenzar la conversación.");
        return;
    }

    addMessageToChat("user", userMessage);

    try {
        const response = await fetch("https://whatsappgpt-l8n6.onrender.com", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                prompt: userMessage,
                brand: activeBrand
            }),
        });

        const data = await response.json();

        if (data.response) {
            addMessageToChat("bot", data.response);
        } else {
            addMessageToChat("bot", "Hubo un error al procesar tu solicitud.");
        }
    } catch (error) {
        addMessageToChat("bot", "Error al conectar con el servidor.");
    }

    searchInput.value = ""; // Limpiar el campo de entrada
}

// Función para guardar la conversación actual
function saveConversation() {
    if (currentConversation.length > 0 && activeBrand) {
        conversationsByBrand[activeBrand].push([...currentConversation]);

        const brandList = document.getElementById(`${activeBrand}-list`);
        const conversationSummary = `Conv. ${conversationsByBrand[activeBrand].length}`;
        const conversationItem = document.createElement("li");
        conversationItem.textContent = conversationSummary;
        conversationItem.addEventListener("click", () => {
            loadConversation(activeBrand, conversationsByBrand[activeBrand].length - 1);
        });

        brandList.appendChild(conversationItem);
    }
}

// Función para cargar una conversación desde la barra lateral
function loadConversation(brand, index) {
    const conversation = conversationsByBrand[brand][index];
    chatHistory.innerHTML = ""; // Limpiar el historial actual
    conversation.forEach(message => {
        addMessageToChat(message.sender, message.message);
    });
}

// Función para cambiar la marca activa y limpiar el chat
function changeActiveBrand(newBrand) {
    if (newBrand !== activeBrand) {
        // Guardar la conversación actual
        saveConversation();

        // Actualizar la marca activa
        activeBrand = newBrand;

        // Limpiar el historial y mostrar mensaje de nueva marca
        chatHistory.innerHTML = "";
        addMessageToChat("bot", `Has seleccionado la marca: ${newBrand}`);
    }
}

// Alternar visibilidad del historial de cada marca en la barra lateral
brandHeaders.forEach(header => {
    header.addEventListener("click", () => {
        const brand = header.dataset.brand;
        changeActiveBrand(brand);
    });
});

// Mostrar el mensaje de bienvenida al cargar
showWelcomeMessage();

// Evento del botón "Enviar"
searchButton.addEventListener("click", sendMessage);

// Evento para enviar mensaje con la tecla "Enter"
searchInput.addEventListener("keypress", (event) => {
    if (event.key === "Enter") {
        event.preventDefault();
        sendMessage();
    }
});

// Evento del botón "Nueva Conversación"
newConversationButton.addEventListener("click", () => {
    saveConversation(); // Guardar la conversación actual
    currentConversation = [];
    showWelcomeMessage();
});

// Evento del botón de menú hamburguesa
menuToggle.addEventListener("click", () => {
    sidebar.classList.toggle("visible");
});
