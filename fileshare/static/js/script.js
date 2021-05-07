
document.getElementById('dlt-button').addEventListener('click', function() {
    document.querySelector('.dlt-modal').style.display = 'flex';
});

document.querySelector('.dlt-close').addEventListener('click', function(){
    document.querySelector('.dlt-modal').style.display = 'none'
})