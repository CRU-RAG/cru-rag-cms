import React from 'react';
import styles from '../Styles/Popup.module.css'; // Import your custom CSS file

const Popup = ({ onClose, children }) => {
    return (
        <div className={styles.popupOverlay}>
            <div className={styles.popupContent}>
                {children}
                <br />
                
            </div>
        </div>
    );
};

export default Popup;
