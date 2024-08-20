var x = 0;
function rot()
{
  if (x % 2 == 0)
  {
    document.getElementById('arrow').style.transform = 'rotate(180deg)';}
  else 
  {
    document.getElementById('arrow').style.transform = 'rotate(0deg)';
  }
  document.getElementById('arrow').style.transition = 'transform 0.3s linear';
x += 1;
}


if ( window.history.replaceState ) 
{
window.history.replaceState( null, null, window.location.href );
}
