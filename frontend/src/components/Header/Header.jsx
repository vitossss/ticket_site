import * as React from 'react';
import { styled } from '@mui/material/styles';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import {Typography} from "@mui/material";

export default function Header() {
    return (
        <Box>
            <AppBar position='static'>
                <Toolbar
                    sx={{
                        display: 'flex',
                        justifyContent: 'space-between',
                        padding: '25px'
                    }}
                >
                    <Box sx={{width: '300px'}}>
                        <Box>
                            Contact info
                        </Box>
                    </Box>
                    <Box>
                        <Typography variant="h4" component="h4">
                            TICKETS
                        </Typography>
                    </Box>
                    <Box sx={{width: '300px'}}>
                        <Box>
                            Login + Cart
                        </Box>
                    </Box>
                </Toolbar>
            </AppBar>
        </Box>
    );
}
