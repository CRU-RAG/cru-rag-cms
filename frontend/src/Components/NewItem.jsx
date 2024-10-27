import React, { useState } from 'react';
import Popup from './Popup';

function NewItem() {
    const [isPopupOpen, setIsPopupOpen] = useState(false);

    const togglePopup = () => {
        setIsPopupOpen(!isPopupOpen);
    };

    return (
        <></>
    );
};

export default NewItem;
