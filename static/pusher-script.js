
// Enable pusher logging for debugging - don't include this in production
Pusher.logToConsole = true;

// configure pusher
const pusher = new Pusher('8d33551ec680cbe8f4e2', {
  cluster: 'eu',
  encrypted: true
});

const soapbox = pusher.subscribe('soapbox');
const clientMessages = pusher.subscribe('private-clientmessages');
const usersChannel = pusher.subscribe('presence-users');

/**
 * UI stuff - I should have used jQuery
 */
function updateAnnoucement(message){
    const announcementDiv = document.getElementById("announcement")
     //empty current contents
     while (announcementDiv.firstChild) {
        announcementDiv.removeChild(announcementDiv.firstChild);
    }
    announcementDiv.appendChild(document.createTextNode(message));
}

function updateUsers(members){
    const membersList = document.getElementById('users-presence');
    
    //empty current contents
    while (membersList.firstChild) {
        membersList.removeChild(membersList.firstChild);
    }

    for (let member in members) {
        const memberElement = document.createElement("li");
            memberElement.appendChild(document.createTextNode(member));
            membersList.appendChild(memberElement)
        }
}

function addMessageToMessagesList(message){
    var node = document.createElement("p");
    var textnode = document.createTextNode(message);
    node.appendChild(textnode);
    document.getElementById('messages').appendChild(node);
}

function sendMessage(){
    const message = document.getElementById('enter-message').value;
    addMessageToMessagesList(message);

    clientMessages.trigger('client-new-message', message);
}

function messageReceived(message){
    addMessageToMessagesList(message);
}

soapbox.bind('announcement', data => {
    updateAnnoucement(data);
});

usersChannel.bind('pusher:subscription_succeeded', () => {

    //stuff you can get from channel and members...
    const me = usersChannel.members.me;
    const userId = me.id;
    const userInfo = me.info;
    const members = usersChannel.members;

    updateUsers(usersChannel.members.members);
});

usersChannel.bind('pusher:member_added', (member) => {
    updateUsers(usersChannel.members.members)
  });

usersChannel.bind('pusher:member_removed', (member) => {
    updateUsers(usersChannel.members.members)
});

clientMessages.bind('client-new-message', (data) => {
    messageReceived(data);
});

console.log("Everything bound - begin here.");






