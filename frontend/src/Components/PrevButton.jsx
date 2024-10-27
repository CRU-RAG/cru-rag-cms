import PrevButtonCss from "../Styles/PrevButton.module.css";

const PrevButton = () => {
  return (
    <div className={PrevButtonCss.addButton}>
      <img src="src/Assets/Images/add.svg" alt="add" />
      <div>New</div>
    </div>
  );
};

export default PrevButton;
