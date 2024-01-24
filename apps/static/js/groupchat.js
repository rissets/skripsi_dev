// main.js
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById('addAgentBtn').addEventListener('click', function () {
        showAgentForm();
    });
});

function showAgentForm() {
    var formHtml = `
        <div id="agentForm" class="mt-3">
            <form id="agentSubmitForm">
                <div class="form-group">
                    <label for="agentName">Nama:</label>
                    <input type="text" class="form-control" id="agentName" name="name" required>
                </div>
                <div class="form-group">
                    <label for="instructionAgent">Instruction:</label>
                    <textarea class="form-control" id="instructionAgent" name="instruction" rows="3" required></textarea>
                </div>
                <button type="submit" class="btn btn-success">Submit</button>
                <button type="button" class="btn btn-secondary ml-2" onclick="cancelForm()">Cancel</button>
            </form>
        </div>
    `;

    document.getElementById('agentFormContainer').innerHTML = formHtml;

    document.getElementById('agentSubmitForm').addEventListener('submit', function (event) {
        event.preventDefault();
        var agentName = document.getElementById('agentName').value;
        var agentInstruction = document.getElementById('instructionAgent').value;
        submitAgent(agentName, agentInstruction, group_chat_id);
    });
}

function cancelForm() {
    document.getElementById('agentFormContainer').innerHTML = '';
}

function submitAgent(agentName, agentInstruction, groupChatId) {

    fetch(create_agent_url, {
        method: 'POST',
        body: JSON.stringify({
            name: agentName,
            instruction: agentInstruction,
            group_chat_id: groupChatId,
        }),
        headers: {
            // Remove the unnecessary headers and set content type
            "content-type": "application/json",
        },

    })
    .then(response => response.json())
    .then(data => {
        showAgentResponse(data);
        document.getElementById('addAgentBtn').parentNode.appendChild(document.getElementById('addAgentBtn'));
        document.getElementById('agentFormContainer').innerHTML = '';
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function showAgentResponse(response) {
    console.log(response);
    var agent_name = response.agent_name;
    var agent_slug = response.agent_slug;
    var agenModalSlug = "#agentModal" + agent_slug;
    var agent_instruction = response.agent_instruction;
    var responseHtml = `
        <a href="#!" class="list-group-item list-group-item-action flex-column align-items-start mb-3" onclick="${showPopup(agent_name, agenModalSlug)}">
            <div class="d-flex w-100 justify-content-between">
              <h5 class="mb-2 h5">${agent_name}</h5>
              <small class="text-muted">Agent</small>
            </div>
            <p class="mb-2">${agent_instruction}</p>
        </a>
    `;
    document.getElementById('agentResponses').insertAdjacentHTML('afterbegin', responseHtml);
}

function showPopup(agentName, agentModalSlug) {
    // Set the content of the modal based on the agent details
    var modalTitle = document.querySelector('.modal-title');
    modalTitle.textContent = `Edit or Delete ${agentName}`;

    // Open the Bootstrap modal
    $(agentModalSlug).modal('show');
}

function closePopup() {
    // Close the Bootstrap modal
    $('#agentModal').modal('hide');
}
