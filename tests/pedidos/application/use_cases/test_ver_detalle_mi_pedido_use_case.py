import pytest
from unittest.mock import AsyncMock, MagicMock
from src.app.pedidos.application.repositories.i_pedido_repository import IPedidoRepository
from src.app.pedidos.application.policies.pedido_policy import PedidoPolicy
from src.app.users.application.repositories.i_user_repository import IUserRepository
from uuid import UUID, uuid4
from src.app.pedidos.application.dtos import PedidoDetalleDTO, LineaDePedidoDTO
from src.app.pedidos.domain.entities import Pedido, LineaDePedido
from src.app.pedidos.domain.value_objects import EstadoPedido
from src.app.users.domain.entities import User
from src.app.users.domain.value_objects import Rol
from datetime import datetime
from decimal import Decimal
from src.app.pedidos.application.exceptions import PedidoNoEncontradoException, AccesoDenegadoException
from src.app.users.application.exceptions import UserNotFoundException

def test_se_puede_importar_ver_detalle_mi_pedido_use_case():
    from src.app.pedidos.application.use_cases.ver_detalle_mi_pedido_use_case import VerDetalleMiPedidoUseCase

def test_use_case_tiene_metodo_execute():
    from src.app.pedidos.application.use_cases.ver_detalle_mi_pedido_use_case import VerDetalleMiPedidoUseCase

    mock_pedido_repository = AsyncMock(spec=IPedidoRepository)
    mock_pedido_policy = PedidoPolicy()
    mock_user_repository = AsyncMock(spec=IUserRepository)
    
    use_case = VerDetalleMiPedidoUseCase(pedido_repository=mock_pedido_repository, pedido_policy=mock_pedido_policy, user_repository=mock_user_repository)
    assert hasattr(use_case, 'execute'), "La clase VerDetalleMiPedidoUseCase debe tener un método execute"

def test_ver_detalle_mi_pedido_use_case_se_puede_instanciar_con_dependencias():
    mock_pedido_repository = AsyncMock(spec=IPedidoRepository)
    mock_pedido_policy = PedidoPolicy()
    mock_user_repository = AsyncMock(spec=IUserRepository)
    
    from src.app.pedidos.application.use_cases.ver_detalle_mi_pedido_use_case import VerDetalleMiPedidoUseCase
    
    use_case = VerDetalleMiPedidoUseCase(
        pedido_repository=mock_pedido_repository, 
        pedido_policy=mock_pedido_policy, 
        user_repository=mock_user_repository
    )
    
    assert use_case.pedido_repository == mock_pedido_repository
    assert use_case.pedido_policy == mock_pedido_policy
    assert use_case.user_repository == mock_user_repository

@pytest.mark.asyncio
async def test_execute_method_signature():
    from src.app.pedidos.application.use_cases.ver_detalle_mi_pedido_use_case import VerDetalleMiPedidoUseCase
    from inspect import iscoroutinefunction, signature

    mock_pedido_repository = AsyncMock(spec=IPedidoRepository)
    mock_pedido_policy = PedidoPolicy()
    mock_user_repository = AsyncMock(spec=IUserRepository)
    use_case = VerDetalleMiPedidoUseCase(
        pedido_repository=mock_pedido_repository, 
        pedido_policy=mock_pedido_policy, 
        user_repository=mock_user_repository
    )

    assert iscoroutinefunction(use_case.execute), "El método execute debe ser una función asíncrona"

    sig = signature(use_case.execute)
    params = list(sig.parameters.keys())

    assert len(params) == 2, f"El método execute debe tener 2 parámetros (pedido_id, usuario_id), pero tiene {len(params)}"
    assert params[0] == "pedido_id", f"El primer parámetro debe ser 'pedido_id', pero es '{params[0]}'"
    assert params[1] == "usuario_id", f"El segundo parámetro debe ser 'usuario_id', pero es '{params[1]}'"
    assert sig.return_annotation == PedidoDetalleDTO, f"El tipo de retorno debe ser PedidoDetalleDTO, pero es {sig.return_annotation}"

@pytest.mark.asyncio
async def test_usuario_puede_ver_su_propio_pedido():
    # Arrange
    mock_pedido_repository = AsyncMock(spec=IPedidoRepository)
    mock_pedido_policy = MagicMock(spec=PedidoPolicy) # Usar MagicMock para métodos síncronos
    mock_user_repository = AsyncMock(spec=IUserRepository)

    usuario_id = uuid4()
    pedido_id = uuid4()
    temporada_id = 1

    # mock_user debe coincidir con el User mínimo creado en el use case
    mock_user = User(
        id=usuario_id,
        email="", 
        contrasena_hasheada="", 
        nombre="", 
        apellidos="", 
        numero_telefono="", 
        rol=Rol.USUARIO, 
        esta_activo=True
    )
    mock_linea = LineaDePedido(
        id=uuid4(),
        pedido_id=pedido_id,
        variante_prenda_id=uuid4(),
        cantidad=2,
        precio_unitario_conxelado=Decimal("10.00"),
        desc_variante_conxelada="Talla M, Color Rojo"
    )
    mock_pedido = Pedido(
        id=pedido_id,
        usuario_id=usuario_id,
        temporada_id=temporada_id,
        estado=EstadoPedido.PENDIENTEPAGO,
        total_calculado=Decimal("20.00"),
        fecha_creacion=datetime.now(),
        lineas=[mock_linea]
    )

    mock_pedido_repository.buscar_por_id_con_detalle.return_value = mock_pedido
    mock_user_repository.buscar_por_id.return_value = mock_user

    # Mockear la política para que siempre permita el acceso en este test
    mock_pedido_policy.ver_pedido.return_value = True # Asignar directamente el valor de retorno

    from src.app.pedidos.application.use_cases.ver_detalle_mi_pedido_use_case import VerDetalleMiPedidoUseCase
    use_case = VerDetalleMiPedidoUseCase(
        pedido_repository=mock_pedido_repository, 
        pedido_policy=mock_pedido_policy, 
        user_repository=mock_user_repository
    )

    # Act
    result_dto = await use_case.execute(pedido_id=pedido_id, usuario_id=usuario_id)

    # Assert
    assert isinstance(result_dto, PedidoDetalleDTO)
    assert result_dto.id == mock_pedido.id
    assert result_dto.usuario_id == mock_pedido.usuario_id
    assert result_dto.total_calculado == mock_pedido.total_calculado
    assert len(result_dto.lineas) == 1
    assert result_dto.lineas[0].id == mock_linea.id

    mock_pedido_repository.buscar_por_id_con_detalle.assert_called_once_with(pedido_id)
    mock_user_repository.buscar_por_id.assert_called_once_with(usuario_id)
    # La política se llama con el usuario mock y el pedido encontrado
    mock_pedido_policy.ver_pedido.assert_called_once_with(mock_user, mock_pedido)

@pytest.mark.asyncio
async def test_ver_detalle_mi_pedido_lanza_excepcion_si_pedido_no_encontrado():
    # Arrange
    mock_pedido_repository = AsyncMock(spec=IPedidoRepository)
    mock_pedido_policy = MagicMock(spec=PedidoPolicy)
    mock_user_repository = AsyncMock(spec=IUserRepository)

    usuario_id = uuid4()
    pedido_id = uuid4()

    mock_pedido_repository.buscar_por_id_con_detalle.return_value = None # Simular que no se encuentra el pedido

    from src.app.pedidos.application.use_cases.ver_detalle_mi_pedido_use_case import VerDetalleMiPedidoUseCase
    use_case = VerDetalleMiPedidoUseCase(
        pedido_repository=mock_pedido_repository, 
        pedido_policy=mock_pedido_policy, 
        user_repository=mock_user_repository
    )

    # Act & Assert
    with pytest.raises(PedidoNoEncontradoException):
        await use_case.execute(pedido_id=pedido_id, usuario_id=usuario_id)

    mock_pedido_repository.buscar_por_id_con_detalle.assert_called_once_with(pedido_id)
    mock_pedido_policy.ver_pedido.assert_not_called() # La política no debería ser llamada si el pedido no existe

@pytest.mark.asyncio
async def test_ver_detalle_mi_pedido_lanza_excepcion_si_usuario_no_encontrado():
    # Arrange
    mock_pedido_repository = AsyncMock(spec=IPedidoRepository)
    mock_pedido_policy = MagicMock(spec=PedidoPolicy)
    mock_user_repository = AsyncMock(spec=IUserRepository)

    usuario_id = uuid4()
    pedido_id = uuid4()

    mock_pedido_repository.buscar_por_id_con_detalle.return_value = Pedido(
        id=pedido_id,
        usuario_id=usuario_id,
        temporada_id=1,
        estado=EstadoPedido.PENDIENTEPAGO,
        total_calculado=Decimal("20.00"),
        fecha_creacion=datetime.now(),
        lineas=[]
    )
    mock_user_repository.buscar_por_id.return_value = None # Simular que no se encuentra el usuario

    from src.app.pedidos.application.use_cases.ver_detalle_mi_pedido_use_case import VerDetalleMiPedidoUseCase
    use_case = VerDetalleMiPedidoUseCase(
        pedido_repository=mock_pedido_repository, 
        pedido_policy=mock_pedido_policy, 
        user_repository=mock_user_repository
    )

    # Act & Assert
    with pytest.raises(UserNotFoundException):
        await use_case.execute(pedido_id=pedido_id, usuario_id=usuario_id)

    mock_pedido_repository.buscar_por_id_con_detalle.assert_called_once_with(pedido_id)
    mock_user_repository.buscar_por_id.assert_called_once_with(usuario_id)
    mock_pedido_policy.ver_pedido.assert_not_called() # La política no debería ser llamada si el usuario no existe

@pytest.mark.asyncio
async def test_ver_detalle_mi_pedido_lanza_excepcion_si_acceso_denegado():
    # Arrange
    mock_pedido_repository = AsyncMock(spec=IPedidoRepository)
    mock_pedido_policy = MagicMock(spec=PedidoPolicy)
    mock_user_repository = AsyncMock(spec=IUserRepository)

    usuario_id = uuid4()
    pedido_id = uuid4()

    mock_user = User(
        id=usuario_id,
        email="", 
        contrasena_hasheada="", 
        nombre="", 
        apellidos="", 
        numero_telefono="", 
        rol=Rol.USUARIO, 
        esta_activo=True
    )
    mock_pedido = Pedido(
        id=pedido_id,
        usuario_id=uuid4(), # ID de usuario diferente para simular que no es el propietario
        temporada_id=1,
        estado=EstadoPedido.PENDIENTEPAGO,
        total_calculado=Decimal("20.00"),
        fecha_creacion=datetime.now(),
        lineas=[]
    )

    mock_pedido_repository.buscar_por_id_con_detalle.return_value = mock_pedido
    mock_user_repository.buscar_por_id.return_value = mock_user
    mock_pedido_policy.ver_pedido.return_value = False # Simular que la política deniega el acceso

    from src.app.pedidos.application.use_cases.ver_detalle_mi_pedido_use_case import VerDetalleMiPedidoUseCase
    use_case = VerDetalleMiPedidoUseCase(
        pedido_repository=mock_pedido_repository, 
        pedido_policy=mock_pedido_policy, 
        user_repository=mock_user_repository
    )

    # Act & Assert
    with pytest.raises(AccesoDenegadoException):
        await use_case.execute(pedido_id=pedido_id, usuario_id=usuario_id)

    mock_pedido_repository.buscar_por_id_con_detalle.assert_called_once_with(pedido_id)
    mock_user_repository.buscar_por_id.assert_called_once_with(usuario_id)
    mock_pedido_policy.ver_pedido.assert_called_once_with(mock_user, mock_pedido)
