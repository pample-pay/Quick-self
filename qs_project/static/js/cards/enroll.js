function btnClick(){

    const text1 = event.target.parentNode.parentNode.childNodes[1];
    const input1 = event.target.parentNode.parentNode.childNodes[3];

    const text2 = event.target.parentNode.parentNode.childNodes[5];
    const input2 = event.target.parentNode.parentNode.childNodes[7];

    const text3 = event.target.parentNode.parentNode.childNodes[9];
    const input3 = event.target.parentNode.parentNode.childNodes[11];

    const text4 = event.target.parentNode.parentNode.childNodes[15];
    const input4 = event.target.parentNode.parentNode.childNodes[17];

    const btn1 = event.target.parentNode;
    const btn2 = event.target.parentNode.nextSibling.nextSibling;

    input1.style.display = 'block';
    input2.style.display = 'block';
    input3.style.display = 'block';
    input4.style.display = 'block';

    text1.style.display = 'none';
    text2.style.display = 'none';
    text3.style.display = 'none';
    text4.style.display = 'none';

    btn1.style.display = 'none';
    btn2.style.display = 'block';

    // input2.childNodes[1].value = {{}};
    // input3.childNodes[1].value
    // input4.childNodes[1].value
    // console.log()
}


    // const select_receipt = document.getElementById('oiling-receipt');
    // select_receipt.value = "{{ form2_oiling_receipt }}";
