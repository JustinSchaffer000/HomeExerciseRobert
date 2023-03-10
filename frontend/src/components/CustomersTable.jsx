import { Box, Card, CardHeader, Paper } from '@mui/material';
import axios from 'axios';
import { useEffect, useState } from 'react';
import DataTable from 'react-data-table-component';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';

const CustomersTable = () => {
	const [customers, setCustomers] = useState([]);
	const [minValue, setMinValue] = useState(0);
	const [maxValue, setMaxValue] = useState(2000);
	const [selectedRow, setSelectedRow] = useState({});
	const [invoices, setInvoices] = useState({});
	const [payments, setPayments] = useState({});

	const getCustomers = async () => {
		try {
			const response = await axios('http://localhost:8000/');

			setInvoices(response.data.customer_invoices)
			setPayments(response.data.invoice_payments)
			const cleanedData = Object.values(response.data.customer).map((customer) => ({
				...customer,
				invoiced_amount: typeof response.data.customer_invoices[customer.name] === "undefined" 
									? customer.amount 
									: customer.amount - response.data.customer_invoices[customer.name].amount,
				invoice_amount: typeof response.data.customer_invoices[customer.name] === "undefined" 
									? 0 
									: response.data.customer_invoices[customer.name].amount
			}))

			setCustomers(Object.values(cleanedData));
		} catch (error) {
			console.log(error);
		}

	};

	const columns = [
		{
			id: 'name',
			name: 'Customer name',
			selector: (row) =>row.name,
			sortable: true,
		},
		{
			id: 'amount',
			name: 'Total',
			selector: (row) =>+row.amount,
			sortable: true,
		},
		{
			id: 'invoiced_amount',
			name: 'Invoiced Amount',
			selector: (row) =>+row.invoiced_amount,
			sortable: true,
		},
		{
			id: 'invoice_amount',
			name: 'Invoice Amount',
			selector: (row) =>+row.invoice_amount,
			sortable: true,
		},
	];

	useEffect(() => {
		getCustomers();
	}, []);

	const handleRowClick = (e) => {
		setSelectedRow(e)
	}

	return (
		<Paper style={{ marginTop: "30px", marginBottom: "30px" }}>
			<DataTable
				title='Custmer List'
				columns={columns}
				data={customers.filter((customer) => {
					return customer.invoiced_amount > minValue && customer.invoiced_amount < maxValue;
				})}
				pagination
				fixedHeader
				fixedHeaderScrollHeight='100vh'
				selectableRowsHighlight
				highlightOnHover
				subHeader
				defaultSortAsc={false}
				defaultSortFieldId={'invoiced_amount'}
				onRowClicked={handleRowClick}
				subHeaderComponent={
					<>
						<TextField
							label="Min Invoiced Amount"
							type="number"
							id="outlined-size-min"
							value={minValue}
							size="small"
							onChange={(e) => setMinValue(+e.target.value)}
						/>
						<TextField
							sx={{ ml: "10px" }}
							label="Max Invoiced Amount"
							type="number"
							id="outlined-size-max"
							value={maxValue}
							size="small"
							onChange={(e) => setMaxValue(+e.target.value)}
						/>
					</>
				}
			/>
			<Card sx={{ p: "20px" }}>
				<CardContent>
					<Typography gutterBottom variant="h5" component="div">
						Customer Name: {selectedRow.name}
					</Typography>
					{invoices[selectedRow.name]?.id.map((id) => <div key={id} style={{ marginTop: "10px" }}>
						<h4>Invoice ID: {id}</h4>
						<TableContainer component={Paper}>
							<Table sx={{ minWidth: 650 }} aria-label="simple table">
								<TableHead>
								<TableRow>
									<TableCell>Reference</TableCell>
									<TableCell align="right">Payment Type</TableCell>
									<TableCell align="right">Amount</TableCell>
								</TableRow>
								</TableHead>
								<TableBody>
									<TableRow
										sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
										>
										<TableCell component="th" scope="row">{payments[id]?.reference}</TableCell>
										<TableCell align="right">{payments[id]?.type}</TableCell>
										<TableCell align="right">{payments[id]?.amount}</TableCell>
									</TableRow>
								</TableBody>
							</Table>
						</TableContainer>
						</div>)
					}

				</CardContent>
			</Card>
		</Paper>
	);
};

export default CustomersTable;
