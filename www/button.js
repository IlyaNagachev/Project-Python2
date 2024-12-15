const button = document.getElementById('MicBtn');

document.addEventListener('keydown', (event) => {
    if (event.code === 'Space') { 
        event.preventDefault();
        button.click(); 
    }
});

