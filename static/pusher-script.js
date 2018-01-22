
function updateAnnoucement(message){
    console.log(`Announcement: ${message}`)
}

function updateUsers(members){
    console.log(`Members:`);
    console.log(members);
}

function sendMessage(message){
    console.log(`Send message: ${message}`)
}

function messageReceived(message){
    console.log(`Received message: ${message}`)
}



// Enable pusher logging for debugging - don't include this in production
Pusher.logToConsole = true;

// configure pusher
const pusher = new Pusher('8d33551ec680cbe8f4e2', {
  cluster: 'eu',
  encrypted: true,
  auth: {
    username = 'zantheman'
  }
});

const soapbox = pusher.subscribe('soapbox');
const clientMessages = pusher.subscribe('private-clientmessages');
const usersChannel = pusher.subscribe('presence-users');

soapbox.bind = pusher.subscribe('announcement', data => {
    updateAnnoucement(data);
});

usersChannel.bind('pusher:subscription_succeeded', () => {

    const me = usersChannel.members.me;
    const userId = me.id;
    const userInfo = me.info;
    const members = usersChannel.members;


    updateUsers(usersChannel.members);
});

usersChannel.bind('pusher:member_added', (member) => {
    updateUsers(usersChannel.members)
  });

usersChannel.bind('pusher:member_removed', (member) => {
    updateUsers(usersChannel.members)
});

clientMessages.bind('new-message', (data) => {
    messageReceived(data);
});







