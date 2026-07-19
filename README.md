# Inter-Airport Stock & Request Management

Moroccan airports mutual aid and inventory management system for technical maintenance teams.

## Objectives
- **Primary:** Resolve the core problem of inter-airport stock and request management.
- **AI Engineering (Advanced):** Implement complex AI architectures and operational intelligence pipelines (e.g., stockout prediction, smart donor-site ranking, NLP catalog matching, and anomaly detection) to provide powerful, data-driven solutions on top of the core workflows.

## Tech Stack
- React
- Vite
- Tailwind CSS
- Supabase
- Google Gemini AI API

## Prerequisites
- Node.js
- Supabase Project

## Run Locally

1. Install dependencies:
   ```bash
   npm install
   ```

2. Set up your environment variables. The `.env` file contains the required keys:
   - `GEMINI_API_KEY`: Your Google Gemini API key.
   - `VITE_SUPABASE_URL`: Your Supabase project URL.
   - `VITE_SUPABASE_ANON_KEY`: Your Supabase project public anonymous key.

   Make sure to update the `.env` file with your credentials if needed.

3. Run the development server:
   ```bash
   npm run dev
   ```

## Database Schema
The Supabase schema is defined in `supabase-schema.sql`. You can run this file in your Supabase SQL Editor to set up the necessary tables and policies.
