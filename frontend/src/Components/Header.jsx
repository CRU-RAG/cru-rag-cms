import Welcome from './Welcome';
import StatsTot from './StatsTot';
import StatsAdmin from './StatsAdmin';

function Header({total}) {
    return (
        <div className="flex justify-between items-center p-4 bg-gray-100">
            <Welcome />
            <div className="flex space-x-8">
                <StatsTot total={total} />
                
            </div>
        </div>
    );
}

export default Header;
