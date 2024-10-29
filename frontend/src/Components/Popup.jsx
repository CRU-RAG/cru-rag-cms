import React from 'react';


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
