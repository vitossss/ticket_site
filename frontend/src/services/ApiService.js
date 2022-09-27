import '../api/api';
import instance from "../api/api";

class ApiService {
    static async getTickets() {
        return instance.get('tickets/')
    }

    static async getTicket(ticket_slug) {
        return instance.get(`tickets/${ticket_slug}`)
    }
}

export default ApiService