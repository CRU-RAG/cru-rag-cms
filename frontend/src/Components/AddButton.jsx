import AddButtonCss from "../Styles/AddButton.module.css";

const AddButton = ({ children }) => {
  return (
    <div className={AddButtonCss.addButton}>
      <img src="src/Assets/Images/add.svg" alt="add" />
      <div>New</div>
    </div>
  );
};

export default AddButton;
