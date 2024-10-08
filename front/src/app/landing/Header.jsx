import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import 'bootstrap/dist/css/bootstrap.min.css'
import useAuth from '../../hook/useAuth'

const Header = ({ onSearch }) => {
	const { isAuthenticated, logout } = useAuth()
	const [searchText, setSearchText] = useState('')

	const handleLogout = () => {
		logout()
		window.location.href = '/'
	}

	const handleSearchChange = (e) => {
		const value = e.target.value
		setSearchText(value)
		onSearch(value) // передаем текст поиска в родительский компонент
	}

	return (
		<header>
			<div className='container'>
				<header className='d-flex flex-wrap align-items-center justify-content-center justify-content-md-between py-3 mb-4 border-bottom'>
					<div>
						<input
							type='search'
							className='rounded border-solid bg-slate-300 form-control'
							style={{ width: '800px' }}
							placeholder='Search...'
							aria-label='Search'
							value={searchText}
							onChange={handleSearchChange} // обработчик изменения текста
						/>
					</div>

					<div className='col-md-3 text-end'>
						{isAuthenticated ? (
							<button
								type='button'
								className='btn btn-outline-primary me-2'
								onClick={handleLogout}
							>
								Logout
							</button>
						) : (
							<>
								<button type='button' className='btn btn-outline-primary me-2'>
									<Link style={{ textDecoration: 'none' }} to='/user/sign-in'>
										Login
									</Link>
								</button>
								<button type='button' className='btn btn-primary'>
									<Link
										style={{ textDecoration: 'none', color: 'white' }}
										to='/user/sign-up'
									>
										Sign-up
									</Link>
								</button>
							</>
						)}
					</div>
				</header>
			</div>
		</header>
	)
}

export default Header
