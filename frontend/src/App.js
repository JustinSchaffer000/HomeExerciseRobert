import './App.css';
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';
import CustomersTable from './components/CustomersTable';

function App() {
	return (
		<section className='container'>
			<CustomersTable />
		</section>
	);
}

export default App;
