# Financial Planner

A modern financial planning application with React frontend and Python backend that helps users track their assets and debts.

## Features

- **Dashboard View**: Display total assets, total debts, and net worth
- **Asset Management**: Add and track real estate, stocks, and cash
- **Debt Management**: Track credit cards, student loans, and mortgages
- **Data Persistence**: All data is stored in a YAML file for easy portability
- **Modern UI**: Clean, light theme with responsive design

## Project Structure

```
fin-agents/
├── backend/          # Python FastAPI backend
├── frontend/         # React TypeScript frontend
└── data/            # YAML data storage
    └── networth.yaml
```

## Getting Started

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the FastAPI server:
   ```bash
   python main.py
   ```

The backend will run on `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the React development server:
   ```bash
   npm start
   ```

The frontend will run on `http://localhost:3000`

## Usage

1. Open the application in your browser at `http://localhost:3000`
2. Use the **Dashboard** tab to view your financial summary
3. Use the **Assets & Debts** tab to:
   - Add new assets (real estate, stocks, cash)
   - Add new debts (credit cards, student loans, mortgages)
   - Delete existing items
4. All data is automatically saved to `data/networth.yaml`

## API Endpoints

- `GET /api/networth` - Get all financial data with summary
- `POST /api/assets/{category}` - Add a new asset
- `POST /api/debts/{category}` - Add a new debt
- `DELETE /api/assets/{category}/{index}` - Delete an asset
- `DELETE /api/debts/{category}/{index}` - Delete a debt

## Data Format

The YAML file structure:
```yaml
assets:
  real_estate: []
  stocks: []
  cash: []
debts:
  credit_card: []
  student_loan: []
  mortgage: []
```

Each item has:
- `type`: Name/identifier
- `value`: Monetary value
- `description`: Optional description