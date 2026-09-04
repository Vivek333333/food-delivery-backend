-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Sep 04, 2026 at 09:23 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `mfd`
--

-- --------------------------------------------------------

--
-- Table structure for table `Banner`
--

CREATE TABLE `Banner` (
  `bid` int(30) NOT NULL,
  `rid` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `restaurant` varchar(255) NOT NULL,
  `images` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Banner`
--

INSERT INTO `Banner` (`bid`, `rid`, `title`, `restaurant`, `images`) VALUES
(1, 28, 'best pizza', 'john Marco\'s Pizza', 'rest_ae301178f982426d9f1cd8afa0d7ff36.jpeg'),
(2, 29, 'best dosa', 'Mr.Disa G', 'rest_fa64bf25fc0f49878785cc9a20e537d5.jpeg');

-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

CREATE TABLE `cart` (
  `uid` int(11) NOT NULL,
  `pid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `cart`
--

INSERT INTO `cart` (`uid`, `pid`) VALUES
(3, 2),
(3, 2),
(3, 1),
(3, 1),
(4, 1),
(4, 2),
(4, 2),
(4, 1),
(14, 23),
(14, 23),
(9, 26),
(14, 33),
(14, 26),
(14, 23),
(14, 23),
(14, 23),
(14, 23),
(14, 23),
(14, 23),
(14, 23),
(14, 23),
(14, 23),
(14, 23),
(14, 23),
(14, 33),
(14, 26),
(17, 117),
(17, 35),
(19, 137),
(11, 143),
(20, 137),
(12, 181);

-- --------------------------------------------------------

--
-- Table structure for table `category`
--

CREATE TABLE `category` (
  `catid` int(11) NOT NULL,
  `rid` int(11) NOT NULL,
  `cat` varchar(255) NOT NULL,
  `images` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `category`
--

INSERT INTO `category` (`catid`, `rid`, `cat`, `images`) VALUES
(39, 29, 'Plain Dosa', 'cat_a3dce7af24d14a9bbb716ea13f96a508.png'),
(40, 29, 'Masala Dosa', 'cat_7901a3b8927f44ff84a0ac54f8204b39.png'),
(41, 29, 'Fancy Dosa', 'cat_0c1aec15fb494f58ac8702881b6b5340.jpeg'),
(42, 29, 'Mysore Masla Dosa', 'cat_531b1be4cb0c471a88bb8f0000e5d633.jpeg'),
(43, 29, 'Special Dosa', 'cat_50a921261fcb4ca7ac932597e4611173.jpeg'),
(44, 29, 'Uttpam', 'cat_8f95235235cd47a8b904b40916f0bfcc.png'),
(46, 29, 'Chinese Fusion ', 'cat_65ba21d9ec604bb8b5d422d68700a959.jpeg'),
(47, 29, 'Green Gotla', 'cat_4bf8e19fa0174f9e83310e5ada109820.jpeg'),
(48, 29, 'Pav Bhaji', 'cat_21cdbc1a3d0c4b9787c75dd34dd02845.png'),
(49, 29, 'Matka Biryani ', 'cat_45c9f7fd61844896a22946c1b5bee1bc.jpeg'),
(50, 29, 'Pulav ', 'cat_17c4fb49309743f1bc35116ce9e8fea3.jpeg'),
(51, 29, 'Beverages', 'cat_e42b1d74e4ca473db4b51c24cf551cfa.jpeg'),
(52, 29, 'Papad', 'cat_6b5b0c32a9d54729b469cab3f392b2ef.jpeg'),
(53, 29, 'French fries ', 'cat_702c7b4a9c64429aacae5d1a65ae6cfd.jpeg'),
(62, 28, 'Pizza (Small)', 'cat_c7301c5d3a5e4ba7a258dfc72461a1cf.png'),
(63, 28, 'Pizza (Medium)', 'cat_fb8ab14ad8694a67954bd15409c82048.png'),
(64, 28, 'Pizza (Large)', 'cat_6b10dc1d8f464217ab5dc08fc23ca182.png'),
(65, 28, 'Special Sides', 'cat_636f4cf2a11c4f409d1cf5689df7a2df.jpeg'),
(66, 28, 'Drinks', 'cat_4f8d98e764044c1f8cbc2dc898136ecb.jpeg'),
(67, 28, 'Burgers', 'cat_90caa033337c4ed494662ff6ffbfa802.png'),
(68, 28, 'Chinese', 'cat_9d5f2394442e4cd591472b9fa7159e7c.png'),
(70, 40, 'Burger ', 'cat_0187dced04554901906331ed676c9a08.jpeg'),
(74, 40, 'Shakes', 'cat_a48c10ba338846e5878b9b6b9738840e.jpeg');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `oid` int(11) NOT NULL,
  `pid` int(11) NOT NULL,
  `uid` int(11) NOT NULL,
  `price` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `address` varchar(255) NOT NULL,
  `paymenttype` varchar(255) NOT NULL,
  `status` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`oid`, `pid`, `uid`, `price`, `quantity`, `address`, `paymenttype`, `status`) VALUES
(1, 1, 2, 522, 1, 'mansa', 'COD', 'delivered'),
(63, 19, 2, 100, 2, 'Fi', 'COD', 'delivered'),
(64, 18, 2, 250, 1, 'Fi', 'COD', 'delivered'),
(65, 19, 2, 100, 3, 'Fi', 'COD', 'delivered'),
(66, 20, 2, 86, 1, 'Fi', 'COD', 'delivered'),
(67, 18, 2, 250, 1, 'Fi', 'COD', 'delivered'),
(68, 21, 2, 240, 2, 'Fi', 'COD', 'delivered'),
(69, 18, 2, 250, 1, 'Fi', 'COD', 'delivered'),
(70, 19, 2, 100, 2, 'Fi', 'COD', 'delivered'),
(71, 22, 2, 999, 3, 'Mansa vraj', 'COD', 'delivered'),
(83, 24, 2, 170, 2, 'Mansa', 'COD', 'delivered'),
(84, 23, 2, 160, 1, 'Mansa', 'COD', 'delivered'),
(98, 25, 2, 170, 1, 'Mansa', 'COD', 'delivered'),
(100, 26, 12, 110, 5, 'CJ4X+QGH, Mansa - Gandhinagar Highway, Mansa, Gujarat, 382845', 'COD', 'delivered'),
(101, 25, 12, 170, 1, 'CJ4X+QGH, Mansa - Gandhinagar Highway, Mansa, Gujarat, 382845', 'COD', 'delivered'),
(102, 26, 12, 110, 1, 'CJ4X+QGH, Mansa - Gandhinagar Highway, Mansa, Gujarat, 382845', 'COD', 'delivered'),
(103, 26, 13, 110, 1, '110, Mansa - Gandhinagar Highway, Shalin Society, Gujarat, 382845', 'COD', 'delivered'),
(106, 23, 12, 160, 1, 'CJ4X+QGH, Mansa - Gandhinagar Highway, Mansa, Gujarat, 382845', 'COD', 'delivered'),
(108, 59, 12, 360, 1, 'CJ4X+QGH, Mansa - Gandhinagar Highway, Mansa, Gujarat, 382845', 'COD', 'delivered'),
(109, 26, 12, 110, 1, 'CJ4X+QGH, Mansa - Gandhinagar Highway, Mansa, Gujarat, 382845', 'COD', 'delivered'),
(110, 26, 12, 110, 1, 'CJ4X+QGH, Mansa - Gandhinagar Highway, Mansa, Gujarat, 382845', 'COD', 'delivered'),
(111, 26, 11, 110, 3, 'FMQ2+H45, Post, Charada, Gujarat, 382810', 'COD', 'delivered');

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `pid` int(11) NOT NULL,
  `rid` int(11) NOT NULL,
  `catid` int(11) NOT NULL,
  `product` varchar(255) NOT NULL,
  `price` int(11) NOT NULL,
  `images` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`pid`, `rid`, `catid`, `product`, `price`, `images`) VALUES
(23, 29, 41, 'Cheese jinny roll dosa', 160, 'product_cbb0d9c44ec14b448b22103c8207cffa.jpeg'),
(24, 29, 41, 'Panner cheese jinni roll', 170, 'product_83ebc3b4df144da1a74e5b99a0b2ac81.jpeg'),
(25, 29, 41, 'Cheese franky dosa', 170, 'product_b06fd04b116b4cd3b9fc0f91d48a5720.jpeg'),
(26, 28, 62, 'Margherita ', 110, 'product_4b798532f2b44403b30791cf7faab264.png'),
(27, 28, 68, 'Manchurian Dry', 100, 'product_f4f0169a777c488992a1ce4dd0dbd172.png'),
(28, 28, 68, 'Manchurian Noodles ', 120, 'product_e19b771ceb5a43e194d1f6d5f0bb09f7.jpeg'),
(29, 28, 68, 'Hakka Noodles', 120, 'product_d13140e6772d4fb5a1deb1ba5c68e77c.jpeg'),
(30, 28, 68, 'Schezwan Noodles', 120, 'product_53c77882b2264ccfa9aecdbd732dabfb.jpeg'),
(31, 28, 65, 'Cheese Garlic Bread ', 80, 'product_634237332b574e5eaf369c7f42d5da39.jpeg'),
(32, 28, 65, 'Corn Garlic Bread ', 90, 'product_2a626db9e94441ccaad9262206dec149.jpeg'),
(33, 28, 65, 'French Fries ', 80, 'product_3bf9cd3819ba4c6785c1b9517df0b095.jpeg'),
(34, 28, 62, 'Double Cheese Margherita ', 190, 'product_d1998ecb0b0e4f6287baf1cfc138061e.jpeg'),
(35, 28, 62, 'Golden Corn', 180, 'product_14d298502ac24b6880429020824b9030.jpeg'),
(36, 28, 62, 'Veggie Delight ', 180, 'product_82a908f7c2b44afead34f7d7001cc0f6.jpeg'),
(37, 28, 62, 'Mexican Delight', 180, 'product_69520ffef0b14e6ba65d491284753af4.jpeg'),
(38, 28, 62, 'Spicy Treat', 180, 'product_8e83edfa46804f68be6876d6fd4b3f0e.jpeg'),
(39, 28, 62, 'Tex Mex', 180, 'product_8b62fc27e7e340b58f06dafecd1e4d46.jpeg'),
(40, 28, 62, 'Mushroom Delight', 180, 'product_53769d37ee134cddb908b6c1ac08af65.jpeg'),
(41, 28, 62, 'American Heat', 180, 'product_ab5c0c95e4bf4a61a6a69bceda1263bb.jpeg'),
(42, 28, 62, 'Balle Balle ', 220, 'product_bbc4ba6d29994676849ff1f076735047.jpeg'),
(43, 28, 62, 'Hawaiian Pizza', 220, 'product_6350875a8ed2436398b68840fe30cefd.jpeg'),
(44, 28, 62, 'Yummy Dummy ', 220, 'product_370964c699a742fa896658e8eeebe121.jpeg'),
(45, 28, 62, 'Chatpata Paneer', 220, 'product_db162b3b0cfb46d5bc70221c4a0c639d.jpeg'),
(46, 28, 62, 'Hot & Spicy', 220, 'product_1ddd8b7847514d2fb12fb07cd510ffc7.jpeg'),
(47, 28, 62, 'Peppy Paneer', 220, 'product_58d3f5c0b7b84523932e95e59695986c.jpeg'),
(48, 28, 62, 'Gujarati Treat', 220, 'product_1b7360916e1747bfbcfcb6acc21c8108.jpeg'),
(49, 28, 62, 'Tikha Paneer Tikka', 220, 'product_e66acde83d184d7995e4d4def706904e.jpeg'),
(50, 28, 62, '7 Cheese', 300, 'product_98de95180a144539b8e1b8638df896cd.jpeg'),
(51, 28, 62, 'Farm Ville', 250, 'product_74c0c8c5c70a4729bb69e0034e8612d7.jpeg'),
(52, 28, 62, 'Paneer Makhani ', 250, 'product_944839d0a0324d32a323dc30000b763e.jpeg'),
(53, 28, 62, 'Fresh Veggie', 250, 'product_ea72b6bbd61b4c5dae11e21390afd7a4.jpeg'),
(54, 28, 62, 'Exotica', 250, 'product_e43c5ed44083497eb9f639187b8a9f5b.jpeg'),
(55, 28, 62, 'Peri Peri ', 250, 'product_13f9a687ef79487fa1c14608c1af1aff.jpeg'),
(56, 28, 62, 'Italian Pizza', 250, 'product_910c741dc1304791bccefee06711fdc3.jpeg'),
(57, 28, 62, 'Amritasari Tandoori Paneer', 250, 'product_c7b7d38c77254bde925bd6e40a79d036.jpeg'),
(58, 28, 63, 'Margherita ', 199, 'product_097353acb9c94a11ba19354319c5cb61.jpeg'),
(59, 28, 64, 'Margherita ', 360, 'product_d0edb4d5a73f44c483d3904e94cce143.jpeg'),
(60, 28, 63, 'Double Cheese Margherita ', 299, 'product_96a6a424aecd4238b7a1440c1fbf824f.jpeg'),
(61, 28, 64, 'Double Cheese Margherita ', 419, 'product_8f0226791db84e49bb307b9079bf5aac.jpeg'),
(62, 28, 63, 'Golden Corn ', 250, 'product_96aeb5b7635642dfae8fd276ab8bbe8a.jpeg'),
(63, 28, 64, 'Golden Corn ', 390, 'product_956f67123f7b4ed98202c838f71ffd69.jpeg'),
(64, 28, 63, 'Veggie Delight ', 250, 'product_3df495c4c84248019aa3141a77ad4c36.jpeg'),
(65, 28, 63, 'Mexican Delight ', 250, 'product_e7476cf0674449d38bb1ce687feb66e0.jpeg'),
(66, 28, 64, 'Veggie Delight ', 390, 'product_8d12e504dabd4434887b4faa809388ee.jpeg'),
(67, 28, 64, 'Mexican Delight ', 390, 'product_72df08fce40449689a7b63490c365ec0.jpeg'),
(68, 28, 63, 'Tex Mex ', 250, 'product_1452e72cc1de475db30ddba94c4da87e.jpeg'),
(69, 28, 64, 'Tex Mex ', 390, 'product_8957508c14e64b22af6d140d43ac8223.jpeg'),
(70, 28, 63, 'Mushroom Delight ', 250, 'product_da3a3cc21dca4ec58ad7cb06c233bb47.jpeg'),
(71, 28, 64, 'Mushroom Delight ', 390, 'product_2b15b87f51ce48d090145cd781c9067b.jpeg'),
(72, 28, 63, 'Spicy Treat', 250, 'product_9896a8d8d7db41b98997b91f577e1c10.jpeg'),
(73, 28, 64, 'Spicy Treat ', 390, 'product_24c26811027742de903572d98cd6c552.jpeg'),
(74, 28, 63, 'American Heat', 250, 'product_bdf550d562fc43d6a1524f117e14c50d.jpeg'),
(75, 28, 64, 'American Heat ', 390, 'product_8f8da7320de44c0b80a69e2760ca8cfe.jpeg'),
(76, 28, 63, 'Balle Balle ', 320, 'product_3dd6c3f1c64b4c6bb98090ab96026af4.jpeg'),
(77, 28, 64, 'Balle Balle ', 420, 'product_dc3256afa0494712880530a1beecb394.jpeg'),
(78, 28, 63, 'Hawaiian ', 320, 'product_72d1be40d86745b2a532d7ae34548db5.jpeg'),
(79, 28, 64, 'Hawaiian ', 420, 'product_5dd9fa659a974c6f8adac458860940b9.jpeg'),
(80, 28, 63, 'Yummy Dummy ', 320, 'product_0ba4ff38a0d34ae9af076d11220d89b9.jpeg'),
(81, 28, 64, 'Yummy Dummy ', 420, 'product_6e2ef503c5c84d828af9a931a9506311.jpeg'),
(82, 28, 64, 'Thin Crust ', 420, 'product_a79ae29d699d497f8d036beb79d4c1ee.jpeg'),
(83, 28, 63, 'Chatpata Paneer ', 320, 'product_16608dc1491646de8e805da77cd5f5e6.jpeg'),
(84, 28, 64, 'Chatpata Paneer ', 420, 'product_0b7462fad1db41dfaccd12d5fe7bb8e9.jpeg'),
(85, 28, 63, 'Hot & Spicy ', 320, 'product_eecc071d99df48af886d25e545fd6c58.jpeg'),
(86, 28, 64, 'Hot & Spicy ', 420, 'product_32092d07ac884421a50fa672083bd140.jpeg'),
(87, 28, 63, 'Peppy Paneer ', 320, 'product_5e4d75eae05c4694b02ae4c5092b1dcd.jpeg'),
(88, 28, 64, 'Peppy Paneer ', 420, 'product_3e303e46206a45abb1fd6c0d63a53fcc.jpeg'),
(89, 28, 63, 'Gujarati Treat ', 320, 'product_9b377570591d4f27934a88bdde08f9d6.jpeg'),
(90, 28, 64, 'Gujarati Treat ', 420, 'product_c2541cb3d190440181c3bc95918f9d8f.jpeg'),
(91, 28, 63, 'Tikha Paneer Tikka ', 320, 'product_b1dd77c044654989b9a0af971b94b9e0.jpeg'),
(92, 28, 64, 'Tikha Paneer Tikka ', 420, 'product_bddcabff79134c2f99bb1f7719ef0629.jpeg'),
(93, 28, 63, '7 Cheese ', 450, 'product_690f06149c9843feb81eec74e19799df.jpeg'),
(94, 28, 64, '7 Cheese ', 649, 'product_fcc6fdb03174495a9915d369cba38565.jpeg'),
(95, 28, 63, 'John Marco\'s', 520, 'product_e0adbdc8a58948e0b951bb628e3b6d42.jpeg'),
(96, 28, 64, 'John Marco\'s ', 700, 'product_49858e6e85f74efa9bd6d6d68e6da4a8.jpeg'),
(97, 28, 63, 'Farm Ville ', 350, 'product_ac6189daff2944039909c9e86cfe9428.jpeg'),
(98, 28, 64, 'Farm Ville ', 450, 'product_5b381baeb0934bf9bcdc7fa4c1ac3830.jpeg'),
(99, 28, 63, 'Paneer Makhani ', 350, 'product_13e6316a7e494f65bb2728788296617b.jpeg'),
(100, 28, 64, 'Paneer Makhani ', 450, 'product_e9835225345c417e8fc4cc51c88d4a36.jpeg'),
(101, 28, 63, 'Fresh Veggie ', 350, 'product_860e10e5e1154e85b3e0680aa6dc8502.jpeg'),
(102, 28, 64, 'Fresh Veggie ', 450, 'product_4759d87add2a4a7a87ed8d78f675b13e.jpeg'),
(103, 28, 63, 'Exotica ', 350, 'product_2eb12f52502947029572f6a0ab897997.jpeg'),
(104, 28, 64, 'Exotica ', 450, 'product_e872ba13842b4adf93391aeea80570de.jpeg'),
(105, 28, 63, 'Peri Peri ', 350, 'product_40c261bd52dd40f9a80b8b8a63017945.jpeg'),
(106, 28, 64, 'Peri Peri ', 450, 'product_89ab20c64caf428abaddaeb391a4e569.jpeg'),
(107, 28, 63, 'Italian Pizza ', 350, 'product_e1e2ab2ab96b41178dedb9ffb40d83bd.jpeg'),
(108, 28, 64, 'Italian Pizza ', 450, 'product_f9ab2f706f804bfebdbc0dbfb68499b7.jpeg'),
(109, 28, 63, 'Amritasari Tandoori Paneer ', 350, 'product_f633be1e9c51458982901f82dcf4c586.jpeg'),
(110, 28, 64, 'Amritasari Tandoori Paneer ', 450, 'product_95ba358596b74a77abdd09fa24963b5f.jpeg'),
(111, 28, 65, 'Peri Peri Fries', 100, 'product_e87997d98a0246afbc7de51982557334.jpeg'),
(112, 28, 65, 'Special Garlic Bread ', 110, 'product_7f01cb3beb0a4eae9cb270182517c480.jpeg'),
(113, 28, 65, 'White Sauce Pasta', 120, 'product_299419ee9ec046debef0b129110f1473.jpeg'),
(114, 28, 65, 'Mexican Pasta', 120, 'product_533eebd1aeba4a9087737b5eefb9a2ab.jpeg'),
(115, 28, 65, 'Red Hot Pasta', 120, 'product_3795e57fd46b4f058615d5b2d4488f29.jpeg'),
(116, 28, 65, 'Cheese Peri Peri Fries ', 140, 'product_65cea881bc3d43abb8878e2b93331f90.jpeg'),
(117, 28, 67, 'Aloo Tikki', 70, 'product_cea14e1382044ddc92f7afa2f0260d2d.jpeg'),
(118, 28, 67, 'Cheese Burger ', 100, 'product_5abcfd28cf3949f58cb4fb6677fdbef8.jpeg'),
(119, 28, 67, 'Mexican Burger ', 120, 'product_9999e29fd266466fb815547b69c674d2.jpeg'),
(120, 28, 67, 'Cheese Peri Peri Burger ', 130, 'product_5763384840d74595b7de40ee5b671d25.jpeg'),
(121, 28, 67, 'Premium Pizza Burger', 130, 'product_05ac9a0729e848b7a6e6ad7d5bd2ca1c.jpeg'),
(122, 28, 67, 'Double Decker Burger ', 150, 'product_23190761538d4999b35c337ba2b30cd2.jpeg'),
(123, 28, 68, 'Manchurian Gravy ', 110, 'product_b743b324e4c14afabef882a1ada9a126.jpeg'),
(124, 28, 68, 'Momos', 90, 'product_ac0232f4032c4804b974ec888164e677.jpeg'),
(125, 28, 66, 'Pepsi 400ml', 20, 'product_24e73c26e3c24f50b49f6a66c4c717f6.png'),
(126, 28, 66, 'Mirinda 400ml', 20, 'product_4747fde166894c13a2fa694d1c101e3a.jpeg'),
(127, 28, 66, 'Mountain Dew 400ml', 20, 'product_56faad53df8445b1b34c08085ba5c2f3.png'),
(128, 28, 66, 'Cold Coffee ', 90, 'product_4c6520fcc4e54a99bf2ec22646e11610.jpeg'),
(129, 28, 66, 'Chocolate Shake', 100, 'product_9552542621bc4699a952d5afcda08157.jpeg'),
(130, 28, 66, 'KitKat Shake', 100, 'product_607eeaea3e0d4b55b527955b1e9e6e23.png'),
(131, 28, 66, 'Oreo Shake', 110, 'product_89c9a99f9ba64253a996f8b44e67bf24.jpeg'),
(132, 28, 66, 'Oreo Coffee', 110, 'product_08fae14b056547aa8651c1dc8df2b29d.jpeg'),
(133, 28, 66, 'Brownie Shake ', 110, 'product_aed1827280e64220ac66850b3b4e17a7.jpeg'),
(134, 28, 66, 'Tomato Soup', 80, 'product_7f2aca3f71c84b52b94ea45c1c63fcda.jpeg'),
(135, 28, 68, 'Masala Maggi', 60, 'product_086cb499035247f3ad66249201edc939.jpeg'),
(136, 28, 68, 'Veg Maggi', 80, 'product_2cc63f1bfccd48aa8c4371b633393968.jpeg'),
(137, 29, 39, 'Plain Paper (Butter & Chrispy)', 60, 'product_bad417eb344e42c6ac6a5fe8e5ae91f9.jpeg'),
(138, 29, 39, 'Baby plain', 60, 'product_f3abe71189fd4ce4a0169277b062ac61.jpeg'),
(139, 29, 39, 'Gwalior Paper ', 90, 'product_5b89fe8a106949ffa704ec6592a06ab8.jpeg'),
(140, 29, 39, 'Nylon paper dosa', 80, 'product_b30a1692fc1148f68e1407bbabfb2734.jpeg'),
(141, 29, 39, 'Cheese onion paper dosa', 100, 'product_462ba25528984cd499e5c6ba74ea30b8.jpeg'),
(142, 29, 39, 'Chocolate plain dosa ', 100, 'product_0459e71ae59b426e97785859b62dcf6c.jpeg'),
(143, 40, 70, 'Aloo Tikki Burger ', 69, 'product_3be49b41e56e4fb497053470288a168a.jpeg'),
(144, 40, 70, 'Cheese Burger ', 90, 'product_a3b26a3b836f439984ff93440cad0476.jpeg'),
(145, 40, 70, 'Mexican Cheese Burger', 120, 'product_e2decde08f504629937ddec4c8df899f.jpeg'),
(146, 40, 70, 'Corn Cheese Burger ', 120, 'product_1f919c73ba884570bef621a075bd9acc.jpeg'),
(147, 40, 70, 'Spicy Paneer Burger ', 120, 'product_79e73ecccd324774b803afdeece6258b.jpeg'),
(148, 40, 70, 'Cheese Peri Peri Burger', 130, 'product_c47de7522e894251b98c2abda0bac596.jpeg'),
(149, 40, 70, 'Makhani Cheese Burst Burger', 140, 'product_b5f33a26a4a147fd971fb6c77fa9d8df.jpeg'),
(150, 40, 70, 'Pizza Burger', 140, 'product_f4602ef1e76e4a618e44f97c2e2cc64b.jpeg'),
(151, 40, 70, 'Royale Paneer Cheese Burger ', 150, 'product_85e1df52edc041c6ae46ae90847e598f.jpeg'),
(152, 40, 70, 'Double Decker Cheese Burger', 160, 'product_062b839fc6cf455cb0b7825853247a02.jpeg'),
(153, 40, 74, 'Cold Coffee ', 80, 'product_fe9f8f9bf95c4cb4bad718a823a615ca.jpeg'),
(154, 40, 74, 'Cold Coffee with Ice Cream ', 100, 'product_3e357e5da6ff4b03a749644de6931d11.jpeg'),
(155, 40, 74, 'Vanilla Shake', 90, 'product_afb040c91ae640a8bdbcbdd4f6f63768.jpeg'),
(156, 40, 74, 'Badam Milk Shake', 100, 'product_69619f4ca40d4a7f873b685dcc53bb9e.jpeg'),
(157, 40, 74, 'Banana Milkshake', 100, 'product_0c8e71001dce4e50ac5b77ba8238c0dd.jpeg'),
(158, 40, 74, 'Butterscotch Milkshake', 110, 'product_14f85ecf201c4b26adc54d71be70a22e.jpeg'),
(159, 40, 74, 'Strawberry Milkshake ', 100, 'product_f7a4a45783cf460a8c552822d1e68cc3.jpeg'),
(160, 40, 74, 'Chocolate Shake', 100, 'product_b9f7e16672994b0897c8b1872c5e3954.jpeg'),
(161, 40, 74, 'Kit Kat Shake', 100, 'product_f4b1a418b3074b72be3f3edb4fe557c3.jpeg'),
(162, 40, 74, 'Oreo Shake', 110, 'product_65bc34c8a5c741e3857eb709ea65b93a.jpeg'),
(163, 40, 74, 'Nutella Shake', 130, 'product_c03c8407cf30409199422165f38bf947.jpeg'),
(164, 40, 74, 'Anjir Shake', 130, 'product_c41c92680e994fc680f5a2f9e653c2cb.jpeg'),
(165, 40, 74, 'Caramel Biscoff Shake', 150, 'product_0353a851bde341a19b4d790365082ba0.jpeg'),
(166, 29, 39, 'Cheese Chili Garlic Nylon Paper', 120, 'product_480f0b43a9694620bb36d1881a205188.jpeg'),
(167, 29, 39, 'Garlic Paper ', 90, 'product_326806e4fa464017a901dab0da327a05.jpeg'),
(168, 29, 39, 'Schezwan Paper', 90, 'product_662a2c8cfeaa49f6aeb889deb2330674.jpeg'),
(169, 29, 39, 'Cheese schezwan dosa', 110, 'product_fcdfdf2e4243483dbb53f12a87c2bba9.jpeg'),
(170, 29, 39, 'Mysore Paper', 90, 'product_ff9d550f9d684ef591036d50f688bd11.jpeg'),
(171, 29, 39, 'Chatni Paper ', 100, 'product_c6eaff2171704289a8d41747801986c5.jpeg'),
(172, 29, 40, 'Masala Dosa', 100, 'product_46230ae954c74bf581521438b928519b.png'),
(173, 29, 40, 'Onion Masala Dosa', 110, 'product_0c7d0b7593cb49008d8b066d3001f5ae.jpeg'),
(174, 29, 40, 'Papper masala Dosa', 140, 'product_89cf504a3d3d4131aa9db5aeb01cfe71.jpeg'),
(175, 29, 40, 'Special cheese Masla Dosa', 150, 'product_0de24a547277457686658556d15ae612.jpeg'),
(176, 29, 40, 'Panner Cheese Masala Dosa', 160, 'product_a36ac4deafdb4c198a0f4b2d7d523972.jpeg'),
(177, 29, 40, 'Green Masala Dosa', 130, 'product_f8844ebcc1f1437b82fcd554629f142c.jpeg'),
(178, 29, 40, 'Green cheese masala Dosa', 150, 'product_7258d577e91741fbae11991789d399a6.jpeg'),
(179, 29, 40, 'Palak paneer masala Dosa ', 150, 'product_59cea98216ce4a3387cdf516575e7e0a.jpeg'),
(180, 29, 40, 'Palak paneer chesse dosa', 160, 'product_626f579266bd48fa92b800e910e6f736.jpeg'),
(181, 29, 40, 'Schezwan masla dosa', 160, 'product_cacb8876a0a849c6ae6cb526f64f8356.jpeg'),
(182, 29, 40, 'Kaju cheese panner masala dosa ', 170, 'product_2454001e6c464810b05df8659c196828.jpeg'),
(183, 29, 40, 'Schezwan cheese panner masala ', 170, 'product_b6745f57005648cba8e96d7a9892ab67.jpeg'),
(184, 29, 41, 'Panner fanky dosa', 170, 'product_8b9fcaf5d62c430badd86ebc3197dc2e.jpeg'),
(185, 29, 41, 'Maggie cheese dosa ', 150, 'product_73ce31804efe4f1a9f31d6dfef6cb788.jpeg'),
(186, 29, 41, 'Panner cheese spring roll ', 180, 'product_b1888b6e30be4cfabd02b69054cce805.jpeg'),
(187, 29, 41, 'paneer sweet corn dosa', 160, 'product_1f920149794243c0a35f7238a13b6fb4.jpeg'),
(188, 29, 41, 'Cheese sweet corn dosa', 170, 'product_a4336120955c48e793b7748e42fa4bbd.jpeg'),
(189, 29, 41, 'Panner chatpata dosa', 180, 'product_8c1b99355ab349cba535085c0655f265.jpeg'),
(190, 29, 41, 'Panner bhurji dosa ', 190, 'product_22f6a5a4cc6f46ca85a18c69eff066c8.jpeg'),
(192, 29, 41, 'Dillkhus dosa', 180, 'product_269055c6d9554dd1bf918cfcae1da58a.jpeg'),
(193, 29, 41, 'Raja rani', 180, 'product_d6aec2f1cac44b5d9c2f7eb64ca9277c.jpeg'),
(194, 29, 41, 'Burj khalifa dosa', 280, 'product_90fbe304116b466e946cad4de456de90.jpeg'),
(195, 29, 41, 'Bombay special dosa', 180, 'product_65f1f3d957bc4bc3a26171c1b63d5458.jpeg'),
(196, 29, 42, 'Mysore Masla dosa', 130, 'product_2edf3b66d18045e38733477595da3dac.jpeg'),
(197, 29, 42, 'Mysore panner tukda dosa', 160, 'product_24b165bad95c43a3a44ff9e12bc9876f.jpeg'),
(198, 29, 42, 'Mysore cheese dosa', 160, 'product_0a0ef7902a1e4c31b0b5eae5dd33375f.jpeg'),
(200, 29, 42, 'Panner cheese mysore dosa', 170, 'product_62b00839820f42e1b56cff61f375cd2c.jpeg'),
(201, 29, 42, 'Sweet corn masala dosa', 160, 'product_15ddfea2c3a74f7b98970bc57bf35df3.jpeg'),
(202, 29, 42, 'Panner sweet corn mysore dosa ', 170, 'product_cdc57d4873114ccab4c60b7ba2988193.jpeg'),
(203, 29, 42, 'Cheese sweet corn mysore dosa', 170, 'product_f4559fdf94e342d08c93bcc77ecdb0e3.jpeg'),
(204, 29, 42, 'Cheese paneer sweet corn mysore ', 180, 'product_248d3992d7a64d32a60685f4f1ec4eb8.jpeg'),
(205, 29, 42, 'Green cheese mysore dosa ', 170, 'product_3cff7407865f4ca8a3213ee391cdb80e.jpeg'),
(206, 29, 42, 'Kaju cheese panner mysore dosa', 220, 'product_7877e93c1901416d8fa569e9d9d13916.jpeg'),
(208, 29, 43, 'Sandwich Dosa', 180, 'product_ace7312de9974e339ba8b960ea487e37.png'),
(209, 29, 43, 'Pizza Dosa', 190, 'product_ae3548a905794c5dbe01bfdad523496a.png'),
(211, 29, 43, 'Ghotala Mysore Dosa', 200, 'product_779164ceaddf4a369f73422bbaef8dd0.png'),
(212, 29, 48, 'Pav bhaji(oil)', 100, 'product_72b94674ccf84177bdcd56f5a19033f5.jpeg'),
(213, 29, 43, 'Matka Dosa', 200, 'product_47e8f01ab2644db7904a1f318b15fbd9.jpeg'),
(215, 29, 48, 'Pav bhaji(butter)', 110, 'product_b5628c1d6bc549d78d5aec9543b12104.jpeg'),
(216, 29, 48, 'Green pav bhaji ', 120, 'product_7a11c8667d334f82906eed5fc98b1c67.jpeg'),
(217, 29, 44, 'Masala Uttapam', 120, 'product_06bc2be077cf43349f61ccdb52456193.png'),
(218, 29, 44, 'Onion Uttapam', 120, 'product_219c55d7999e47578044d71ae32df9ff.png'),
(219, 29, 48, 'Green cheese bhaji', 140, 'product_9a915eb43e3d4c0cab6ca7fd77ef032c.jpeg'),
(220, 29, 44, 'Cheese Onion Uttapam', 140, 'product_2ecf691a91884f0baf64e3ee84e13da9.png'),
(221, 29, 48, 'Cheese pav bhaji', 140, 'product_5462536c150c4b43b075a4a7bb6a7dc6.jpeg'),
(222, 29, 44, 'Tomato Uttapam', 130, 'product_f6cee35192684d63a1c618d8ba5e016f.png'),
(223, 29, 44, 'Mix Veg. Uttapam ', 130, 'product_ae43c5fd8cac4967b36b2d1b8ffa1e33.png'),
(224, 29, 48, 'Panner pav bhaji', 140, 'product_0c59343b95a24b25b81ac4c2c7b96be1.jpeg'),
(225, 29, 44, 'Mix Veg. Cheese Uttapam', 150, 'product_d5b09f289c93432db132b3050d91af2f.png'),
(226, 29, 44, 'Cheese Paneer Uttapam ', 150, 'product_69b4379023134746866df65ca75dd887.png'),
(227, 29, 48, 'Cheese paneer pav bhaji', 150, 'product_dbb1e2102e694c3291a94234a89a9b56.jpeg'),
(228, 29, 44, 'Sp Mr. Dosa Uttapam', 180, 'product_f32233f8201c47d58ef95d3c876e6d07.png'),
(229, 29, 48, 'Kaju Cheese pavbhaji', 170, 'product_91da129019aa42b6b2bbb8204d23eb0f.jpeg'),
(230, 29, 48, 'Pav(butter)', 20, 'product_8d859c200bc1474ea53c5a48cf314b2a.jpeg'),
(231, 29, 46, 'American Cheese Chopsy Dosa', 160, 'product_e816d54f81bf4fce9b6dd895da644834.png'),
(232, 29, 46, 'Cheese Chinese Dosa', 170, 'product_baa42fbaa81c4a3782cedf40115885bc.png'),
(233, 29, 46, 'Paneer Chilli Cheese Dosa', 180, 'product_dd6b5c0a9df142db930cabf0b91b47ca.jpeg'),
(234, 29, 47, 'Green Ghotala', 190, 'product_93070145656845e7b3837e5a50ff2edf.png'),
(235, 29, 47, 'Paneer Ghotala', 220, 'product_1a8eadaa17b942cfb2621cbbe9dbeefe.png'),
(236, 29, 47, 'Veg Cheese Paneer Ghotala', 250, 'product_f27ca4ab82c74f29bd67e0c880f704f3.png'),
(237, 29, 51, 'Butter Milk', 20, 'product_370db6ea498848e5aa7ab9d63fc78ba0.jpeg'),
(239, 29, 51, 'Cold Drink', 20, 'product_ec641ad37d2b47a186abb5d5d0b75dbd.png'),
(240, 29, 51, 'Maaza', 25, 'product_60d9e0c03e0844668519d9b8d9f15def.png'),
(241, 29, 52, 'Roasted Papad', 10, 'product_75563d77978f4df0ad1ad6a33edca0d5.png'),
(242, 29, 52, 'Fry Papad', 20, 'product_4b2c1dd707ad495691c0047999d27903.png'),
(243, 29, 52, 'Masala Papad', 30, 'product_c144c8ce66b94be0ae998a5d4ca4c1dc.png'),
(244, 29, 53, 'Salted French Fries ', 70, 'product_cd04dc82fe93431581c0a1c9abee0be1.png'),
(245, 29, 53, 'Masala French Fries ', 80, 'product_4c8ced799e104b2796e767d674233f8b.png'),
(246, 29, 48, 'Masala pav', 120, 'product_fb0f0a6997a94aaca5bad24aad3f60fd.jpeg'),
(247, 29, 53, 'Peri Peri French Fries ', 90, 'product_0ed7156def6a429c8e6e7ab62b1fd223.png'),
(248, 29, 48, 'Special masala cheese pav', 140, 'product_ac1f7b71266042a4a4f071e83711b70d.jpeg'),
(249, 29, 50, 'Pulav oil/butter ', 100, 'product_582c98fa24e94d38ac8bb4266baf84f2.jpeg'),
(250, 29, 50, 'Cheese pulav', 130, 'product_831087c03ac546ab93723e9779042d2e.jpeg'),
(251, 29, 49, 'Veg. Matka Biryani', 200, 'product_3dae780f29a840d59f8327c008167579.png'),
(252, 29, 49, 'Panjabi Matka Biryani ', 220, 'product_4abbf3c932ed49338d75f7a7fe3b7253.jpeg'),
(253, 29, 50, 'kaju paneer cheese pulao', 160, 'product_0f060d8a5c3a4446a2e3d945482cae3d.jpeg'),
(254, 29, 49, 'Hyderabadi Matka Biryani', 240, 'product_75c0674739c44556a59ce39d6ed9705b.png'),
(256, 29, 50, 'kaju paneer cheese singapuri pulav', 180, 'product_78bca490a68f4571903476674210c0f4.jpeg'),
(257, 29, 50, 'Biryani pulav(butter)', 130, 'product_f109deae70374e8194c3fb22d94ed957.jpeg'),
(258, 29, 50, 'Kaju panner cheese hyderabadi pulav', 180, 'product_63c84588b54d4b64bcfeb0f562f4ca5d.jpeg');

-- --------------------------------------------------------

--
-- Table structure for table `restaurants`
--

CREATE TABLE `restaurants` (
  `rid` int(11) NOT NULL,
  `rname` varchar(255) NOT NULL,
  `images` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `restaurants`
--

INSERT INTO `restaurants` (`rid`, `rname`, `images`) VALUES
(28, 'John Marco\'s Pizza', 'rest_ae301178f982426d9f1cd8afa0d7ff36.jpeg'),
(29, 'Mr.Dosa G', 'rest_fa64bf25fc0f49878785cc9a20e537d5.jpeg'),
(30, 'Hotel Siya', 'rest_a1df330f49264bf08e6ddbab2306e2f1.png'),
(32, 'Shree Ram Zumpadi Restaurant', 'rest_2137974612c24bda947e877e9f3742bf.png'),
(34, 'Honest', 'rest_8f12736622c04066aa17406d998d5678.png'),
(38, 'British Pizza', 'rest_5673f4035c5d425797ea3356294630ec.png'),
(40, 'Burger & Shakes', 'rest_13d50e0cbad343f69513b05640e9a263.jpeg');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `uid` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `phone` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`uid`, `username`, `phone`) VALUES
(2, 'Deepu', '9978590175'),
(7, 'Manan', '7359237995'),
(10, 'Visu', '7096220564'),
(11, 'Savan', '9106051303'),
(12, 'Vivek', '8511916534'),
(13, 'priyank190990@gmail.com', '9274458290'),
(14, 'Divya', '9157545758'),
(15, 'Ketul Sathvara', '9624189310'),
(16, 'Kadiya Vraj', '8401118577'),
(17, 'Urvi P', '7016761095'),
(18, 'Bittu', '6359338014'),
(19, 'Rahil', '6354731177'),
(20, 'Aadi Thakor', '9106461484'),
(21, 'Chirag Goswami', '7600453317');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Banner`
--
ALTER TABLE `Banner`
  ADD PRIMARY KEY (`bid`),
  ADD KEY `rid` (`rid`);

--
-- Indexes for table `category`
--
ALTER TABLE `category`
  ADD PRIMARY KEY (`catid`),
  ADD KEY `rid` (`rid`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`oid`),
  ADD KEY `pid` (`pid`),
  ADD KEY `orders_ibfk_1` (`uid`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`pid`),
  ADD KEY `rid` (`rid`),
  ADD KEY `products_ibfk_2` (`catid`);

--
-- Indexes for table `restaurants`
--
ALTER TABLE `restaurants`
  ADD PRIMARY KEY (`rid`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`uid`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Banner`
--
ALTER TABLE `Banner`
  MODIFY `bid` int(30) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `category`
--
ALTER TABLE `category`
  MODIFY `catid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=75;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `oid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=112;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `pid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=259;

--
-- AUTO_INCREMENT for table `restaurants`
--
ALTER TABLE `restaurants`
  MODIFY `rid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `uid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Banner`
--
ALTER TABLE `Banner`
  ADD CONSTRAINT `Banner_ibfk_1` FOREIGN KEY (`rid`) REFERENCES `restaurants` (`rid`);

--
-- Constraints for table `category`
--
ALTER TABLE `category`
  ADD CONSTRAINT `rid` FOREIGN KEY (`rid`) REFERENCES `restaurants` (`rid`);

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `user` (`uid`);

--
-- Constraints for table `products`
--
ALTER TABLE `products`
  ADD CONSTRAINT `products_ibfk_1` FOREIGN KEY (`rid`) REFERENCES `restaurants` (`rid`),
  ADD CONSTRAINT `products_ibfk_2` FOREIGN KEY (`catid`) REFERENCES `category` (`catid`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
