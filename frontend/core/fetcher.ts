import axios from 'axios';
import { apiUrl } from './environment';

export const fetcher = axios.create({ baseURL: apiUrl });
