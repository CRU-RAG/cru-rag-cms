function Welcome() {
    return (
        <div className="flex items-center space-x-4 h-20"> {/* Set height for the outer div */}
            <img
                className="h-full w-auto rounded-full cursor-pointer hover:scale-110 transition-transform" // Use h-full to make it the same height as the parent
                src="src/Assets/Images/Avatar.svg"
                alt="avatar"
            />
            <div>
                <h1 className="text-[30px] font-semibold">Welcome Back, Admin</h1>
                <p className="text-[16px] text-gray-600">Track, manage and add Bible <br /> Knowledges</p>
            </div>
        </div>
    );
}

export default Welcome;
